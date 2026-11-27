from pathlib import Path

from app.ingestion.chunker import chunk_document
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.schemas import DocumentChunk


def process_pdf(
    file_path: Path,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[DocumentChunk]:
    """Extract a PDF's text and convert its pages into searchable chunks."""

    pages = load_pdf(file_path)

    chunks: list[DocumentChunk] = []

    for page in pages:
        page_chunks = chunk_document(
            page,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        chunks.extend(page_chunks)

    return chunks
