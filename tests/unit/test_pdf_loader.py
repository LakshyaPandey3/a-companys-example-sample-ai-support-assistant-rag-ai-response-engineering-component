
import pytest
from pypdf import PdfWriter
from pypdf.generic import (
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
)

from app.ingestion.pdf_loader import load_pdf


@pytest.fixture
def sample_pdf(tmp_path):
    """Create a temporary two-page PDF for testing."""

    pdf_path = tmp_path / "sample_policy.pdf"

    writer = PdfWriter()

    writer.add_blank_page(width=300, height=300)
    writer.add_blank_page(width=300, height=300)

    writer.add_metadata(
        {
            "/Title": "Sample Policy",
        }
    )

    with pdf_path.open("wb") as pdf_file:
        writer.write(pdf_file)

    return pdf_path



def create_text_page(writer, text):
    """Add a PDF page containing extractable text."""

    page = writer.add_blank_page(width=300, height=300)

    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )

    page[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/Font"): DictionaryObject(
                {
                    NameObject("/F1"): font,
                }
            )
        }
    )

    content = DecodedStreamObject()
    content.set_data(
        f"BT /F1 12 Tf 50 250 Td ({text}) Tj ET".encode("ascii")
    )

    page[NameObject("/Contents")] = content



def test_load_pdf_rejects_nonexistent_file(tmp_path):
    """Verify that missing PDF files raise FileNotFoundError."""

    missing_file = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        load_pdf(missing_file)


def test_load_pdf_rejects_non_pdf_file(tmp_path):
    """Verify that files with unsupported extensions are rejected."""

    text_file = tmp_path / "sample.txt"
    text_file.write_text("Sample content.", encoding="utf-8")

    with pytest.raises(ValueError, match="Only PDF files are supported"):
        load_pdf(text_file)


def test_load_pdf_returns_empty_list_for_blank_pages(sample_pdf):
    """Verify that pages without extractable text are skipped."""

    pages = load_pdf(sample_pdf)

    assert pages == []

def test_load_pdf_extracts_text_and_preserves_page_numbers(tmp_path):
    """Verify actual text extraction and original page numbering."""

    pdf_path = tmp_path / "text_policy.pdf"

    writer = PdfWriter()

    create_text_page(writer, "First page policy content.")
    create_text_page(writer, "Second page policy content.")

    with pdf_path.open("wb") as pdf_file:
        writer.write(pdf_file)

    pages = load_pdf(pdf_path)

    assert len(pages) == 2

    assert pages[0].document_id == "text_policy"
    assert pages[0].document_name == "text_policy.pdf"
    assert pages[0].page_number == 1
    assert "First page policy content." in pages[0].text

    assert pages[1].page_number == 2
    assert "Second page policy content." in pages[1].text