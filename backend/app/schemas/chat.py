from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class SourceReference(BaseModel):
    document_id: str
    title: str
    category: Optional[str] = None
    author: Optional[str] = None
    source_url: Optional[str] = None
    snippet: str
    score: float

class ChatMessageRequest(BaseModel):
    session_id: Optional[str] = None  # None indicates create a new session
    message: str = Field(..., min_length=1)

class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    sources: Optional[List[SourceReference]] = None
    is_crisis: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: Optional[List[MessageResponse]] = None

    class Config:
        from_attributes = True

class SessionUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)

class ChatStreamChunk(BaseModel):
    type: str  # "delta" | "sources" | "crisis" | "done" | "session"
    content: Optional[str] = None
    sources: Optional[List[SourceReference]] = None
    session_id: Optional[str] = None
    message_id: Optional[str] = None

