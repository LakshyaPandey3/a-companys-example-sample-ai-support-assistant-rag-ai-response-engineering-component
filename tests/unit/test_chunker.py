
import pytest

from app.ingestion.chunker import chunk_document
from app.ingestion.schemas import DocumentPage


@pytest.fixture
def sample_page():
    """Create a sample document page for chunking tests."""

    return DocumentPage(
        document_id="sample-policy-001",
        document_name="sample_policy.pdf",
        page_number=3,
        text="abcdefghijkl",
    )


def test_chunk_document_returns_single_chunk_for_short_text(sample_page):
    """Verify that short text remains a single chunk."""

    chunks = chunk_document(
        sample_page,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(chunks) == 1
    assert chunks[0].text == "abcdefghijkl"


def test_chunk_document_splits_text_with_overlap(sample_page):
    """Verify chunk boundaries and overlapping characters."""

    chunks = chunk_document(
        sample_page,
        chunk_size=5,
        chunk_overlap=2,
    )

    assert [chunk.text for chunk in chunks] == [
        "abcde",
        "defgh",
        "ghijk",
        "jkl",
    ]


def test_chunk_document_preserves_source_metadata(sample_page):
    """Verify that every chunk retains its original source information."""

    chunks = chunk_document(
        sample_page,
        chunk_size=5,
        chunk_overlap=2,
    )

    for chunk in chunks:
        assert chunk.document_id == "sample-policy-001"
        assert chunk.document_name == "sample_policy.pdf"
        assert chunk.page_number == 3


def test_chunk_document_generates_unique_chunk_ids(sample_page):
    """Verify that different chunks receive different identifiers."""

    chunks = chunk_document(
        sample_page,
        chunk_size=5,
        chunk_overlap=2,
    )

    chunk_ids = [chunk.chunk_id for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))


def test_chunk_document_generates_deterministic_ids(sample_page):
    """Verify that identical input produces identical chunk IDs."""

    first_result = chunk_document(
        sample_page,
        chunk_size=5,
        chunk_overlap=2,
    )

    second_result = chunk_document(
        sample_page,
        chunk_size=5,
        chunk_overlap=2,
    )

    first_ids = [chunk.chunk_id for chunk in first_result]
    second_ids = [chunk.chunk_id for chunk in second_result]

    assert first_ids == second_ids


def test_chunk_document_rejects_zero_chunk_size(sample_page):
    """Verify that zero chunk size is rejected."""

    with pytest.raises(ValueError, match="greater than zero"):
        chunk_document(sample_page, chunk_size=0)


def test_chunk_document_rejects_negative_overlap(sample_page):
    """Verify that negative overlap is rejected."""

    with pytest.raises(ValueError, match="cannot be negative"):
        chunk_document(
            sample_page,
            chunk_size=5,
            chunk_overlap=-1,
        )


def test_chunk_document_rejects_overlap_equal_to_chunk_size(sample_page):
    """Verify that overlap must be smaller than chunk size."""

    with pytest.raises(ValueError, match="smaller than chunk size"):
        chunk_document(
            sample_page,
            chunk_size=5,
            chunk_overlap=5,
        )


def test_chunk_document_returns_empty_list_for_whitespace(sample_page):
    """Verify that whitespace-only page content produces no chunks."""

    whitespace_page = sample_page.model_copy(
        update={"text": "   \n   "}
    )

    chunks = chunk_document(whitespace_page)

    assert chunks == []
