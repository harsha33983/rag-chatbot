from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DocumentItem(BaseModel):
    id: str
    title: str
    category: Optional[str] = "General Mental Wellness"
    author: Optional[str] = None
    organization: Optional[str] = None
    source_url: Optional[str] = None
    publication_date: Optional[str] = None
    licensing: Optional[str] = None
    content: str

class IngestRequest(BaseModel):
    documents: Optional[List[DocumentItem]] = None
    reload_default_library: bool = False

class KnowledgeStatusResponse(BaseModel):
    total_vectors: int
    collection_name: str
    embedding_model: str
    status: str
    sample_categories: List[str] = []

class DocumentUploadResponse(BaseModel):
    message: str
    document_id: str
    chunks_created: int
    title: str

