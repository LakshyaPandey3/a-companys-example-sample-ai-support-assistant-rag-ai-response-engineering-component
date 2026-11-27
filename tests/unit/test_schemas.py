
import pytest
from pydantic import ValidationError

from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    SourceReference,
)


def test_valid_chat_request():
    """Verify that a valid user question is accepted."""

    request = ChatRequest(
        question="What documents are required to apply?"
    )

    assert request.question == "What documents are required to apply?"


def test_empty_question_is_rejected():
    """Verify that an empty question is rejected."""

    with pytest.raises(ValidationError):
        ChatRequest(question="")


def test_question_exceeding_maximum_length_is_rejected():
    """Verify that questions longer than 2000 characters are rejected."""

    with pytest.raises(ValidationError):
        ChatRequest(question="a" * 2001)


def test_valid_source_reference():
    """Verify that a valid document source reference is accepted."""

    source = SourceReference(
        document_name="Application_Guide.pdf",
        page_number=3,
        chunk_id="chunk_001",
    )

    assert source.document_name == "Application_Guide.pdf"
    assert source.page_number == 3
    assert source.chunk_id == "chunk_001"


def test_invalid_page_number_is_rejected():
    """Verify that page numbers must start from 1."""

    with pytest.raises(ValidationError):
        SourceReference(
            document_name="Application_Guide.pdf",
            page_number=0,
            chunk_id="chunk_001",
        )


def test_valid_chat_response():
    """Verify that an answer with source references is accepted."""

    response = ChatResponse(
        answer="The application requires the listed documents.",
        sources=[
            SourceReference(
                document_name="Application_Guide.pdf",
                page_number=3,
                chunk_id="chunk_001",
            )
        ],
        status="answered",
    )

    assert response.status == "answered"
    assert len(response.sources) == 1
    assert response.sources[0].page_number == 3


def test_unsupported_response_status_is_rejected():
    """Verify that unsupported response statuses are rejected."""

    with pytest.raises(ValidationError):
        ChatResponse(
            answer="I could not find sufficient information.",
            status="unknown",
        )


def test_health_response():
    """Verify that the health response uses the expected status."""

    response = HealthResponse()

    assert response.status == "healthy"
