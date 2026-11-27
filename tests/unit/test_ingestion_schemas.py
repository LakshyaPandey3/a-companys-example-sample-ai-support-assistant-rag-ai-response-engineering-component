
import pytest
from pydantic import ValidationError

from app.ingestion.schemas import DocumentPage


def test_document_page_accepts_valid_data():
    """Verify that a valid document page can be created."""

    page = DocumentPage(
        document_id="sample-policy-001",
        document_name="sample_policy.pdf",
        page_number=1,
        text="This is sample policy content.",
    )

    assert page.document_id == "sample-policy-001"
    assert page.document_name == "sample_policy.pdf"
    assert page.page_number == 1
    assert page.text == "This is sample policy content."


def test_document_page_rejects_empty_document_id():
    """Verify that an empty document ID is rejected."""

    with pytest.raises(ValidationError):
        DocumentPage(
            document_id="",
            document_name="sample_policy.pdf",
            page_number=1,
            text="Sample content.",
        )


def test_document_page_rejects_invalid_page_number():
    """Verify that page numbers must start from one."""

    with pytest.raises(ValidationError):
        DocumentPage(
            document_id="sample-policy-001",
            document_name="sample_policy.pdf",
            page_number=0,
            text="Sample content.",
        )


def test_document_page_rejects_empty_text():
    """Verify that empty extracted text is rejected."""

    with pytest.raises(ValidationError):
        DocumentPage(
            document_id="sample-policy-001",
            document_name="sample_policy.pdf",
            page_number=1,
            text="",
        )
