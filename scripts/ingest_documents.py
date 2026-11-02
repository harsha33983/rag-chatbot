"""
Standalone Document Ingestion Script for MindCare AI RAG Knowledge Base.
Supports ingesting 500+ curated mental wellness resources, raw text files, markdown files, and PDFs.
"""
import sys
import os
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.services.rag_service import rag_service
from knowledge_base.mental_wellness_500 import KNOWLEDGE_DOCUMENTS_500

def ingest_500_library():
    print(f"Ingesting {len(KNOWLEDGE_DOCUMENTS_500)} curated mental health resources into Qdrant...")
    total_chunks = rag_service.ingest_documents_batch(KNOWLEDGE_DOCUMENTS_500, batch_size=128)
    status = rag_service.get_status()
    print(f"\nIngestion Complete!")
    print(f"  Total Resources Processed: {len(KNOWLEDGE_DOCUMENTS_500)}")
    print(f"  Total Chunks Indexed in Qdrant: {total_chunks}")
    print(f"  Collection Name: '{status['collection_name']}'")
    print(f"  Total Vectors in Store: {status['total_vectors']}")

def ingest_directory(directory_path: str):
    dir_path = Path(directory_path)
    if not dir_path.exists():
        print(f"Directory not found: {directory_path}")
        return

    files = list(dir_path.glob("**/*.*"))
    supported = [f for f in files if f.suffix.lower() in [".txt", ".md", ".pdf"]]
    print(f"Found {len(supported)} documents in {directory_path}...")

    docs = []
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
            docs.append({
                "id": doc_id,
                "title": title,
                "content": text,
                "category": "Uploaded Document",
                "source_url": str(file_path)
            })

    total_chunks = rag_service.ingest_documents_batch(docs)
    print(f"\nDirectory indexing complete! Total {total_chunks} chunks added across {len(docs)} documents.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MindCare AI RAG Ingestion")
    parser.add_argument("--dir", type=str, help="Path to directory containing .txt, .md, or .pdf files")
    parser.add_argument("--curated", action="store_true", default=True, help="Ingest 500+ curated mental wellness documents")

    args = parser.parse_args()

    if args.dir:
        ingest_directory(args.dir)
    else:
        ingest_500_library()
