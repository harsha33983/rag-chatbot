"""
Standalone Document Ingestion Script for MindCare AI RAG Knowledge Base.
Supports ingesting default curated library, raw text files, markdown files, and PDFs.
"""
import sys
import os
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.services.rag_service import rag_service
from knowledge_base.mental_wellness_library import KNOWLEDGE_DOCUMENTS

def ingest_curated_library():
    print(f"Ingesting {len(KNOWLEDGE_DOCUMENTS)} foundational mental wellness documents...")
    total_chunks = 0
    for doc in KNOWLEDGE_DOCUMENTS:
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
        print(f"  Indexed '{doc['title']}' -> {chunks} chunks")
    print(f"\nIngestion Complete! Total {total_chunks} chunks indexed into Qdrant collection '{rag_service.collection_name}'.")

def ingest_directory(directory_path: str):
    dir_path = Path(directory_path)
    if not dir_path.exists():
        print(f"Directory not found: {directory_path}")
        return

    files = list(dir_path.glob("**/*.*"))
    supported = [f for f in files if f.suffix.lower() in [".txt", ".md", ".pdf"]]
    print(f"Found {len(supported)} documents in {directory_path}...")

    total_indexed = 0
    for file_path in supported:
        title = file_path.stem.replace("_", " ").title()
        doc_id = f"doc_{file_path.stem.lower()}"
        text = ""

        if file_path.suffix.lower() in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif file_path.suffix.lower() == ".pdf":
            try:
                import fitz
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text() + "\n"
            except Exception as e:
                print(f"  Error reading PDF {file_path.name}: {e}")
                continue

        if text.strip():
            chunks = rag_service.ingest_document(
                doc_id=doc_id,
                title=title,
                content=text,
                category="Clinical Library",
                source_url=str(file_path)
            )
            total_indexed += chunks
            print(f"  Indexed '{title}' ({file_path.name}) -> {chunks} chunks")

    print(f"\nDirectory indexing complete! Total {total_indexed} chunks added.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MindCare AI RAG Ingestion")
    parser.add_argument("--dir", type=str, help="Path to directory containing .txt, .md, or .pdf files")
    parser.add_argument("--curated", action="store_true", default=True, help="Ingest built-in curated mental wellness documents")

    args = parser.parse_args()

    if args.dir:
        ingest_directory(args.dir)
    else:
        ingest_curated_library()

