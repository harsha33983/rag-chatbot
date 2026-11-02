import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.core.security import get_password_hash
from backend.app.models.user import User
from datetime import datetime, timezone
from backend.app.api.auth import router as auth_router
from backend.app.api.chat import router as chat_router
from backend.app.api.knowledge import router as knowledge_router
from backend.app.api.health import router as health_router
from backend.app.services.rag_service import rag_service
from knowledge_base.mental_wellness_library import KNOWLEDGE_DOCUMENTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("mindcare")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure SQL tables exist
    logger.info("Initializing relational database tables...")
    Base.metadata.create_all(bind=engine)

    # Seed demo account if not exists
    try:
        with SessionLocal() as db:
            demo_user = db.query(User).filter(User.email == "demo@mindcare.ai").first()
            if not demo_user:
                demo_user = User(
                    name="Demo User",
                    email="demo@mindcare.ai",
                    password_hash=get_password_hash("MindCarePass123!"),
                    created_at=datetime.now(timezone.utc)
                )
                db.add(demo_user)
                db.commit()
                logger.info("Default demo account seeded: demo@mindcare.ai / MindCarePass123!")
    except Exception as e:
        logger.warning(f"Demo user seeding warning: {e}")

    # Ingest core curated knowledge if vector DB has 0 items
    try:
        status_info = rag_service.get_status()
        if status_info.get("total_vectors", 0) == 0:
            logger.info("Vector store is empty. Auto-ingesting foundational mental wellness library...")
            for doc in KNOWLEDGE_DOCUMENTS:
                rag_service.ingest_document(
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
            logger.info("Curated knowledge base successfully indexed.")
    except Exception as e:
        logger.warning(f"Initial knowledge base seeding warning: {e}")

    yield
    logger.info("Shutting down MindCare AI backend services.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MindCare AI - Empathetic Mental Wellness Chatbot with RAG & Clinical Safety Protocols",
    lifespan=lifespan
)

# CORS configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development & local pairing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(knowledge_router, prefix=settings.API_V1_STR)
app.include_router(health_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }

