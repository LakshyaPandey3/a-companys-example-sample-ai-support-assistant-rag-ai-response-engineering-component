
from pathlib import Path

from pypdf import PdfReader

from app.ingestion.schemas import DocumentPage


def load_pdf(file_path: Path) -> list[DocumentPage]:
    """Extract text from a PDF and return structured page objects."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    reader = PdfReader(file_path)

    document_id = file_path.stem

    pages: list[DocumentPage] = []

    for page_number, pdf_page in enumerate(reader.pages, start=1):
        extracted_text = pdf_page.extract_text()

        if not extracted_text or not extracted_text.strip():
            continue

        pages.append(
            DocumentPage(
                document_id=document_id,
                document_name=file_path.name,
                page_number=page_number,
                text=extracted_text.strip(),
            )
        )

    return pages