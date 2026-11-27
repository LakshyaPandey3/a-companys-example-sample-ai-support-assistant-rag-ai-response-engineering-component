from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    """Represents text extracted from a single document page."""

    document_id: str = Field(
        min_length=1,
        description="Unique identifier assigned to the source document.",
    )

    document_name: str = Field(
        min_length=1,
        description="Original name of the source document.",
    )

    page_number: int = Field(
        ge=1,
        description="One-based page number in the source document.",
    )

    text: str = Field(
        min_length=1,
        description="Text extracted from the document page.",
    )




class DocumentChunk(BaseModel):
    """Represents a searchable text chunk with source metadata."""

    chunk_id: str = Field(
        min_length=1,
        description="Unique identifier assigned to this text chunk.",
    )

    document_id: str = Field(
        min_length=1,
        description="Identifier of the original source document.",
    )

    document_name: str = Field(
        min_length=1,
        description="Original name of the source document.",
    )

    page_number: int = Field(
        ge=1,
        description="Original page number containing this chunk.",
    )

    text: str = Field(
        min_length=1,
        description="Text content of the chunk.",
    )
