from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path
import os

# Project root directory (parent of backend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_SQLITE_PATH = (BASE_DIR / "mindcare.db").as_posix()

class Settings(BaseSettings):
    PROJECT_NAME: str = "MindCare AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Database: Default to persistent SQLite in project root
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")

    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-mindcare-key-change-in-production-2024-jwt")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Vector Database (Qdrant)
    VECTOR_DATABASE_URL: Optional[str] = os.getenv("VECTOR_DATABASE_URL", None)
    VECTOR_STORAGE_PATH: str = os.getenv("VECTOR_STORAGE_PATH", str(BASE_DIR / "qdrant_storage"))
    VECTOR_COLLECTION: str = os.getenv("VECTOR_COLLECTION", "mental_health_knowledge")

    # Embedding & RAG
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "100"))
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))

    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" | "openai" | "offline"
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)

    # Conversational memory
    MAX_MEMORY_TURNS: int = 30

    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
