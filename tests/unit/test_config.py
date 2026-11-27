
import pytest
from pydantic import ValidationError

from app.core.config import Settings, settings


def test_settings_load_successfully():
    """Verify that the application settings load with valid values."""

    assert settings.llm_provider == "groq"
    assert settings.llm_model == "openai/gpt-oss-120b"
    assert settings.embedding_model == "BAAI/bge-small-en-v1.5"
    assert settings.chunk_size == 1000
    assert settings.chunk_overlap == 200
    assert settings.top_k == 5


def test_chunk_overlap_must_be_smaller_than_chunk_size():
    """Verify that invalid chunk configuration is rejected."""

    with pytest.raises(ValidationError):
        Settings(
            chunk_size=1000,
            chunk_overlap=1000,
        )


def test_chunk_size_must_be_positive():
    """Verify that chunk size cannot be zero."""

    with pytest.raises(ValidationError):
        Settings(chunk_size=0)
