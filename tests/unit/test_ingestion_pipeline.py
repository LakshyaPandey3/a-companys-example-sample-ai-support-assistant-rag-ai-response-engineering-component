

from pypdf import PdfWriter

from app.ingestion.pipeline import process_pdf


def create_text_page(writer, text):
    """Add a PDF page containing extractable text."""

    from pypdf.generic import (
        DecodedStreamObject,
        DictionaryObject,
        NameObject,
    )

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



def test_process_pdf_extracts_and_chunks_multiple_pages(tmp_path):
    """Verify complete PDF extraction and chunking across pages."""

    pdf_path = tmp_path / "sample_policy.pdf"

    writer = PdfWriter()

    create_text_page(writer, "ABCDEFGHIJKL")
    create_text_page(writer, "MNOPQRSTUVWX")

    with pdf_path.open("wb") as pdf_file:
        writer.write(pdf_file)

    chunks = process_pdf(
        pdf_path,
        chunk_size=5,
        chunk_overlap=2,
    )

    assert len(chunks) == 8

    assert [chunk.text for chunk in chunks] == [
    "ABCDE",
    "DEFGH",
    "GHIJK",
    "JKL",
    "MNOPQ",
    "PQRST",
    "STUVW",
    "VWX",
    ]

    assert all(
        chunk.document_name == "sample_policy.pdf"
        for chunk in chunks
    )

    assert [chunk.page_number for chunk in chunks] == [
        1, 1, 1, 1,
        2, 2, 2, 2,
    ]
