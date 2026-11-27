from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for submitting a question to the RAG service."""

    question: str = Field(
        min_length=1,
        max_length=2000,
        description="The user's question about the available knowledge base.",
    )


class SourceReference(BaseModel):
    """Reference to a document passage used to generate an answer."""

    document_name: str = Field(
        min_length=1,
        description="Name of the source document.",
    )
    page_number: int = Field(
        ge=1,
        description="One-based page number in the source document.",
    )
    chunk_id: str = Field(
        min_length=1,
        description="Unique identifier of the retrieved document chunk.",
    )


class ChatResponse(BaseModel):
    """Structured response returned by the RAG service."""

    answer: str = Field(
        min_length=1,
        description="The generated answer or fallback message.",
    )
    sources: list[SourceReference] = Field(
        default_factory=list,
        description="Document references supporting the answer.",
    )
    status: Literal["answered", "insufficient_evidence"] = Field(
        description="Indicates whether sufficient supporting evidence was found.",
    )


class HealthResponse(BaseModel):
    """Response schema for the service health endpoint."""

    status: Literal["healthy"] = "healthy"
