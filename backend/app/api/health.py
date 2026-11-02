from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.core.database import get_db
from backend.app.core.config import settings
from backend.app.services.rag_service import rag_service

router = APIRouter(tags=["System"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    vector_status = "connected"
    try:
        status_info = rag_service.get_status()
        vector_status = status_info["status"]
    except Exception as e:
        vector_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_status,
        "vector_store": vector_status
    }

