import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from backend.app.core.config import settings
from backend.app.utils.text_splitter import RecursiveCharacterTextSplitter
from backend.app.schemas.chat import SourceReference

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.model_name = model_name
        self._model = None
        self._dimension = 384

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading SentenceTransformer embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                logger.warning(f"Failed to load sentence_transformers ({e}). Using robust fallback vectorizer.")
                self._model = "fallback"
        return self._model

    def encode(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        try:
            m = self.model
            if m != "fallback" and hasattr(m, "encode"):
                embeddings = m.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
                return embeddings.tolist()
        except Exception as e:
            logger.warning(f"SentenceTransformer encoding error: {e}. Falling back to deterministic hashing.")

        # Robust deterministic fallback vectorizer (384 dimensions)
        import hashlib
        import math
        fallback_vecs = []
        for text in texts:
            vec = [0.0] * self._dimension
            words = text.lower().split()
            for i, word in enumerate(words):
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                idx = h % self._dimension
                vec[idx] += 1.0 / (1.0 + math.log(i + 1))
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vec = [x / norm for x in vec]
            fallback_vecs.append(vec)
        return fallback_vecs

class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService(settings.EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.collection_name = settings.VECTOR_COLLECTION
        self._init_qdrant()

    def _init_qdrant(self):
        try:
            if settings.VECTOR_DATABASE_URL:
                logger.info(f"Connecting to remote Qdrant: {settings.VECTOR_DATABASE_URL}")
                self.client = QdrantClient(url=settings.VECTOR_DATABASE_URL)
            else:
                os.makedirs(settings.VECTOR_STORAGE_PATH, exist_ok=True)
                logger.info(f"Using local Qdrant storage at {settings.VECTOR_STORAGE_PATH}")
                self.client = QdrantClient(path=settings.VECTOR_STORAGE_PATH)

            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                logger.info(f"Creating Qdrant collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
        except Exception as e:
            logger.warning(f"Error initializing Qdrant disk storage: {e}. Falling back to in-memory Qdrant instance.")
            self.client = QdrantClient(":memory:")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def ingest_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        category: str = "General",
        author: Optional[str] = None,
        organization: Optional[str] = None,
        source_url: Optional[str] = None,
        publication_date: Optional[str] = None,
        licensing: Optional[str] = None
    ) -> int:
        """
        Split a document into chunks, generate embeddings, and store them in Qdrant.
        Returns the number of chunks indexed.
        """
        chunks = self.text_splitter.split_text(content)
        if not chunks:
            return 0

        # Delete any existing chunks for this doc_id first
        self.delete_document(doc_id)

        embeddings = self.embedding_service.encode(chunks)
        points = []

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}_{i}"))
            payload = {
                "document_id": doc_id,
                "chunk_index": i,
                "title": title,
                "category": category,
                "author": author or "MindCare AI Wellness",
                "organization": organization or "MindCare Knowledge Center",
                "source_url": source_url or "https://mindcare.ai/resources",
                "publication_date": publication_date or "2024",
                "licensing": licensing or "Educational",
                "content": chunk
            }
            points.append(PointStruct(id=point_id, vector=embedding, payload=payload))

        self.client.upsert(collection_name=self.collection_name, points=points)
        logger.info(f"Successfully ingested {len(points)} chunks for doc {doc_id} ('{title}')")
        return len(points)

    def search(self, query: str, top_k: int = None, threshold: float = None) -> List[SourceReference]:
        """
        Convert query into embedding, search Qdrant, filter by threshold,
        and return formatted SourceReference objects.
        """
        top_k = top_k or settings.TOP_K
        threshold = threshold if threshold is not None else settings.SIMILARITY_THRESHOLD

        if not query or not query.strip():
            return []

        query_vectors = self.embedding_service.encode([query])
        if not query_vectors:
            return []

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vectors[0],
                limit=top_k
            )
        except Exception as e:
            logger.error(f"Error querying Qdrant: {e}")
            return []

        references = []
        for hit in results:
            score = float(hit.score)
            if score >= threshold:
                payload = hit.payload or {}
                content = payload.get("content", "")
                snippet = content[:300] + "..." if len(content) > 300 else content
                references.append(SourceReference(
                    document_id=payload.get("document_id", "unknown"),
                    title=payload.get("title", "Resource"),
                    category=payload.get("category", "Mental Wellness"),
                    author=payload.get("author", "Mental Health Guide"),
                    source_url=payload.get("source_url"),
                    snippet=snippet,
                    score=round(score, 4)
                ))

        return references

    def get_status(self) -> Dict[str, Any]:
        """
        Returns statistics about the vector store collection.
        """
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            total = info.points_count if hasattr(info, "points_count") else 0
        except Exception:
            total = 0

        return {
            "total_vectors": total,
            "collection_name": self.collection_name,
            "embedding_model": settings.EMBEDDING_MODEL,
            "status": "ready"
        }

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks associated with a document_id.
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=doc_id)
                        )
                    ]
                )
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id} from Qdrant: {e}")
            return False

rag_service = RAGService()

