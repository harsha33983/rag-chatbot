import re
from typing import List, Dict, Any

class RecursiveCharacterTextSplitter:
    """
    A robust, sentence-aware text chunker with configurable token/word budget
    and overlap for RAG ingestion.
    """
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        separators: List[str] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        text = text.strip()
        if not text:
            return []

        # Quick estimate: 1 word ~ 1.3 tokens or approx word count
        words = text.split()
        if len(words) <= self.chunk_size:
            return [text]

        chunks = []
        current_chunk = []
        current_length = 0

        # Break into paragraphs or sentences first
        sentences = re.split(r'(?<=[.?!])\s+', text)

        for sent in sentences:
            sent_words = sent.split()
            sent_len = len(sent_words)

            if current_length + sent_len <= self.chunk_size:
                current_chunk.append(sent)
                current_length += sent_len
            else:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                
                # Calculate overlap
                overlap_words = []
                overlap_len = 0
                for prev_sent in reversed(current_chunk):
                    p_words = prev_sent.split()
                    if overlap_len + len(p_words) <= self.chunk_overlap:
                        overlap_words.insert(0, prev_sent)
                        overlap_len += len(p_words)
                    else:
                        break

                current_chunk = overlap_words + [sent]
                current_length = sum(len(s.split()) for s in current_chunk)

        if current_chunk:
            final_text = " ".join(current_chunk)
            if not chunks or chunks[-1] != final_text:
                chunks.append(final_text)

        return chunks

