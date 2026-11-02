import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from backend.app.models.user import User
from backend.app.api.deps import get_current_user
from backend.app.services.rag_service import rag_service
from backend.app.schemas.knowledge import (
    IngestRequest,
    KnowledgeStatusResponse,
    DocumentUploadResponse
)
from knowledge_base.mental_wellness_library import KNOWLEDGE_DOCUMENTS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/knowledge", tags=["Knowledge Management"])

@router.get("/status", response_model=KnowledgeStatusResponse)
def get_knowledge_status():
    status_info = rag_service.get_status()
    # List unique categories present in default library
    categories = sorted(list(set(d["category"] for d in KNOWLEDGE_DOCUMENTS)))
    return KnowledgeStatusResponse(
        total_vectors=status_info["total_vectors"],
        collection_name=status_info["collection_name"],
        embedding_model=status_info["embedding_model"],
        status=status_info["status"],
        sample_categories=categories
    )

@router.post("/ingest")
def ingest_documents(
    payload: Optional[IngestRequest] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Ingest default curated mental health knowledge base or user-provided batch.
    """
    docs_to_ingest = []
    if payload and payload.documents:
        docs_to_ingest = [d.model_dump() for d in payload.documents]
    elif payload and payload.reload_default_library or not payload or not payload.documents:
        docs_to_ingest = KNOWLEDGE_DOCUMENTS

    total_chunks = 0
    for doc in docs_to_ingest:
        chunks = rag_service.ingest_document(
            doc_id=doc["id"],
            title=doc["title"],
            content=doc["content"],
            category=doc.get("category", "General"),
            author=doc.get("author"),
            organization=doc.get("organization"),
            source_url=doc.get("source_url"),
            publication_date=doc.get("publication_date"),
            licensing=doc.get("licensing")
        )
        total_chunks += chunks

    return {
        "message": f"Successfully ingested {len(docs_to_ingest)} documents into {total_chunks} chunks.",
        "documents_processed": len(docs_to_ingest),
        "total_chunks": total_chunks
    }

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    category: Optional[str] = Form("Uploaded Resources"),
    current_user: User = Depends(get_current_user)
):
    filename = file.filename or "uploaded_file.txt"
    doc_title = title if title else filename.rsplit(".", 1)[0].replace("_", " ").title()
    doc_id = f"doc_{uuid.uuid4().hex[:10]}"

    contents = await file.read()
    text = ""

    # Check extension
    if filename.lower().endswith(".txt") or filename.lower().endswith(".md"):
        try:
            text = contents.decode("utf-8")
        except UnicodeDecodeError:
            text = contents.decode("latin-1", errors="ignore")
    elif filename.lower().endswith(".pdf"):
        # Extract PDF text using pypdfium2 or fitz
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=contents, filetype="pdf")
            for page in doc:
                text += page.get_text() + "\n"
        except Exception:
            try:
                import pypdfium2 as pdfium
                pdf = pdfium.PdfDocument(contents)
                for page in pdf:
                    text_page = page.get_textpage()
                    text += text_page.get_text_range() + "\n"
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Could not extract text from PDF: {str(e)}"
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload PDF, TXT, or Markdown (.md) files."
        )

    if not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file contains no extractable text."
        )

    chunks_created = rag_service.ingest_document(
        doc_id=doc_id,
        title=doc_title,
        content=text,
        category=category,
        author=f"Uploaded by {current_user.name}",
        organization="User Uploaded Resource"
    )

    return DocumentUploadResponse(
        message="Document uploaded and indexed successfully into vector memory.",
        document_id=doc_id,
        chunks_created=chunks_created,
        title=doc_title
    )

@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    success = rag_service.delete_document(document_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not delete document chunks."
        )
    return {"message": f"Document {document_id} deleted successfully."}

