import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.api.deps import get_current_user
from backend.app.schemas.chat import (
    ChatMessageRequest,
    MessageResponse,
    SessionResponse,
    SessionUpdate,
    SourceReference
)
from backend.app.services.safety_service import safety_service
from backend.app.services.sentiment_service import sentiment_service
from backend.app.services.rag_service import rag_service
from backend.app.services.memory_service import memory_service
from backend.app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=MessageResponse)
def send_chat_message(
    chat_req: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main RAG Chat Pipeline:
    1. Resolve or create user session.
    2. Record user message in SQL memory.
    3. Run Crisis Safety Screening before any RAG or LLM generation.
    4. If crisis is detected, generate safety response and bypass ordinary generation.
    5. If safe, retrieve context from Vector DB (RAG) and conversation history (up to 30 turns).
    6. Generate empathetic grounded response using LLM.
    7. Save assistant response and return with source citations.
    """
    # 1. Resolve or create session
    session_id = chat_req.session_id
    if session_id:
        session = memory_service.get_session_by_id(db, session_id, current_user.id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation session not found or does not belong to you."
            )
    else:
        # Create new session
        session = memory_service.create_session(db, current_user.id, title="New Conversation")
        session_id = session.id

    # 2. Save user message
    user_msg = memory_service.add_message(
        db=db,
        session_id=session_id,
        role="user",
        content=chat_req.message.strip(),
        sources=None,
        is_crisis=False
    )

    # Auto-generate title if this is the first interaction
    memory_service.auto_generate_title(db, session_id, chat_req.message)

    # 3. Crisis Safety Screening (Mandatory Pre-Generation Guardrail)
    crisis_result = safety_service.evaluate_message(chat_req.message)

    if crisis_result.is_crisis:
        logger.warning(f"Crisis detected for user {current_user.id} in session {session_id}: {crisis_result.crisis_type}")
        # Save crisis response
        assistant_msg = memory_service.add_message(
            db=db,
            session_id=session_id,
            role="assistant",
            content=crisis_result.crisis_response,
            sources=None,
            sentiment={"label": "crisis", "confidence": 1.0, "tone_strategy": "Emergency Escalation"},
            is_crisis=True
        )
        return MessageResponse(
            id=assistant_msg.id,
            session_id=session_id,
            role="assistant",
            content=assistant_msg.content,
            sources=None,
            is_crisis=True,
            sentiment={"label": "crisis", "confidence": 1.0, "tone_strategy": "Emergency Escalation"},
            created_at=assistant_msg.created_at
        )

    # 4. Six-Class Sentiment Analysis & Real-Time Tone Adaptation
    sentiment_result = sentiment_service.predict(chat_req.message)
    sentiment_payload = {
        "label": sentiment_result.label,
        "confidence": sentiment_result.confidence,
        "tone_strategy": sentiment_result.tone_strategy
    }

    # 5. Memory retrieval (preserving 30+ conversational turns)
    history_records = memory_service.get_session_history(db, session_id, current_user.id)
    # Convert previous messages to LLM format (excluding the current user message just saved)
    formatted_history = [
        {"role": m.role, "content": m.content}
        for m in history_records[:-1]
    ]

    # 6. RAG Retrieval from Knowledge Base
    retrieved_sources = rag_service.search(chat_req.message)

    # 7. Response generation with Tone Adaptation
    response_text = llm_service.generate_response(
        user_message=chat_req.message,
        conversation_history=formatted_history,
        retrieved_sources=retrieved_sources,
        tone_instruction=sentiment_result.tone_instruction
    )

    # Convert sources to serializable dicts
    sources_data = [s.model_dump() for s in retrieved_sources] if retrieved_sources else None

    # 8. Save assistant message with sources and detected sentiment
    assistant_msg = memory_service.add_message(
        db=db,
        session_id=session_id,
        role="assistant",
        content=response_text,
        sources=sources_data,
        sentiment=sentiment_payload,
        is_crisis=False
    )

    return MessageResponse(
        id=assistant_msg.id,
        session_id=session_id,
        role="assistant",
        content=assistant_msg.content,
        sources=retrieved_sources if retrieved_sources else None,
        is_crisis=False,
        sentiment=sentiment_payload,
        created_at=assistant_msg.created_at
    )

@router.get("/sessions", response_model=List[SessionResponse])
def get_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = memory_service.get_user_sessions(db, current_user.id)
    return [SessionResponse.model_validate(s) for s in sessions]

@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = memory_service.create_session(db, current_user.id, title="New Conversation")
    return SessionResponse.model_validate(session)

@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = memory_service.get_session_by_id(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found."
        )
    return SessionResponse.model_validate(session)

@router.patch("/sessions/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: str,
    update_data: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = memory_service.update_session_title(db, session_id, current_user.id, update_data.title)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    return SessionResponse.model_validate(session)

@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = memory_service.delete_session(db, session_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    return {"message": "Session deleted successfully."}

