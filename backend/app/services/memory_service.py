import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from backend.app.models.session import Session as SessionModel
from backend.app.models.message import Message as MessageModel
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class MemoryService:
    @staticmethod
    def create_session(db: Session, user_id: str, title: str = "New Conversation") -> SessionModel:
        session = SessionModel(
            user_id=user_id,
            title=title,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_user_sessions(db: Session, user_id: str) -> List[SessionModel]:
        """
        Retrieve all sessions belonging to the user, ordered by most recently updated.
        """
        return (
            db.query(SessionModel)
            .filter(SessionModel.user_id == user_id)
            .order_by(SessionModel.updated_at.desc())
            .all()
        )

    @staticmethod
    def get_session_by_id(db: Session, session_id: str, user_id: str) -> Optional[SessionModel]:
        """
        Enforce strict user-level authorization: users can only access their own sessions.
        """
        return (
            db.query(SessionModel)
            .filter(SessionModel.id == session_id, SessionModel.user_id == user_id)
            .first()
        )

    @staticmethod
    def update_session_title(db: Session, session_id: str, user_id: str, title: str) -> Optional[SessionModel]:
        session = MemoryService.get_session_by_id(db, session_id, user_id)
        if not session:
            return None
        session.title = title
        session.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def delete_session(db: Session, session_id: str, user_id: str) -> bool:
        session = MemoryService.get_session_by_id(db, session_id, user_id)
        if not session:
            return False
        db.delete(session)
        db.commit()
        return True

    @staticmethod
    def add_message(
        db: Session,
        session_id: str,
        role: str,
        content: str,
        sources: Optional[List[dict]] = None,
        sentiment: Optional[dict] = None,
        is_crisis: bool = False
    ) -> MessageModel:
        message = MessageModel(
            session_id=session_id,
            role=role,
            content=content,
            sources=sources,
            sentiment=sentiment,
            is_crisis=is_crisis,
            created_at=datetime.now(timezone.utc)
        )
        db.add(message)
        
        # Update session updated_at
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session:
            session.updated_at = datetime.now(timezone.utc)
            
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_session_history(
        db: Session,
        session_id: str,
        user_id: str,
        max_turns: int = settings.MAX_MEMORY_TURNS
    ) -> List[MessageModel]:
        """
        Retrieve up to max_turns conversational turns (1 turn = user + assistant = 2 messages).
        Strictly validates user ownership.
        """
        session = MemoryService.get_session_by_id(db, session_id, user_id)
        if not session:
            return []

        limit_messages = max_turns * 2
        # Query latest messages ordered by creation
        messages = (
            db.query(MessageModel)
            .filter(MessageModel.session_id == session_id)
            .order_by(MessageModel.created_at.asc())
            .all()
        )
        
        # If exceeds turn limit, slice the most recent
        if len(messages) > limit_messages:
            messages = messages[-limit_messages:]
            
        return messages

    @staticmethod
    def auto_generate_title(db: Session, session_id: str, first_message: str):
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session and (session.title == "New Conversation" or not session.title):
            clean_text = first_message.strip()
            # Generate a clean 3-6 word title
            words = clean_text.split()
            if len(words) > 6:
                title = " ".join(words[:6]) + "..."
            else:
                title = clean_text
            session.title = title[:80]
            db.commit()

memory_service = MemoryService()

