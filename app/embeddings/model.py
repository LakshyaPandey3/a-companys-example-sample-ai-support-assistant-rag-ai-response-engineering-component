from fastembed import TextEmbedding

from app.core.config import settings


class EmbeddingModel:
    """Generate text embeddings using a locally running FastEmbed model."""

    def __init__(
        self,
        model_name: str | None = None,
        batch_size: int = 256,
    ) -> None:
        if batch_size <= 0:
            raise ValueError("Batch size must be greater than zero.")

        self.model_name = model_name or settings.embedding_model
        self.batch_size = batch_size
        self._model: TextEmbedding | None = None

    def _get_model(self) -> TextEmbedding:
        """Initialize the embedding model only when it is first needed."""
        if self._model is None:
            self._model = TextEmbedding(
                model_name=self.model_name,
                lazy_load=True,
            )

        return self._model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Convert a list of text strings into numerical embedding vectors."""
        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError(
                "Input texts cannot contain empty or whitespace-only values."
            )

        embeddings = self._get_model().embed(
            documents=texts,
            batch_size=self.batch_size,
        )

        return [[float(value) for value in embedding] for embedding in embeddings]
