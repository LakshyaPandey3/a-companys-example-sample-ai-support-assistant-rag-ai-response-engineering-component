from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM provider configuration
    llm_provider: Literal["groq"] = "groq"
    groq_api_key: SecretStr = SecretStr("")
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "openai/gpt-oss-120b"

    # Embedding configuration
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Vector database configuration
    qdrant_path: Path = Path("./storage/qdrant")

    # RAG configuration
    chunk_size: int = Field(default=1000, gt=0)
    chunk_overlap: int = Field(default=200, ge=0)
    top_k: int = Field(default=5, gt=0)

    @model_validator(mode="after")
    def validate_chunk_configuration(self):
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
            )
        return self


settings = Settings()
