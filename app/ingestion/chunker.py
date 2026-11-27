from uuid import NAMESPACE_URL, uuid5

from app.core.config import settings
from app.ingestion.schemas import DocumentChunk, DocumentPage


def chunk_document(
    page: DocumentPage,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[DocumentChunk]:
    """Split a document page into overlapping chunks with source metadata."""

    size = chunk_size if chunk_size is not None else settings.chunk_size
    overlap = (
        chunk_overlap
        if chunk_overlap is not None
        else settings.chunk_overlap
    )

    if size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0:
        raise ValueError("Chunk overlap cannot be negative.")

    if overlap >= size:
        raise ValueError("Chunk overlap must be smaller than chunk size.")

    text = page.text.strip()

    if not text:
        return []

    chunks: list[DocumentChunk] = []
    start = 0
    chunk_index = 1

    while start < len(text):
        end = start + size
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunk_id = str(
                uuid5(
                    NAMESPACE_URL,
                    (
                        f"{page.document_id}:"
                        f"{page.page_number}:"
                        f"{chunk_index}:"
                        f"{chunk_text}"
                    ),
                )
            )

            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    document_name=page.document_name,
                    page_number=page.page_number,
                    text=chunk_text,
                )
            )

            chunk_index += 1

        if end >= len(text):
            break

        start = end - overlap

    return chunks
