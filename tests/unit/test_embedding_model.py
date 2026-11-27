from unittest.mock import MagicMock, patch

import pytest

from app.core.config import settings
from app.embeddings.model import EmbeddingModel


def test_embedding_model_uses_configured_model_by_default():
    model = EmbeddingModel()

    assert model.model_name == settings.embedding_model
    assert model.batch_size == 256
    assert model._model is None


def test_embedding_model_rejects_invalid_batch_size():
    with pytest.raises(ValueError, match="Batch size must be greater than zero"):
        EmbeddingModel(batch_size=0)


def test_embedding_model_initializes_lazily():
    with patch("app.embeddings.model.TextEmbedding") as mock_embedding:
        model = EmbeddingModel()

        mock_embedding.assert_not_called()

        model._get_model()

        mock_embedding.assert_called_once_with(
            model_name=settings.embedding_model,
            lazy_load=True,
        )


def test_embed_texts_returns_vectors_in_input_order():
    fake_model = MagicMock()
    fake_model.embed.return_value = iter(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]
    )

    model = EmbeddingModel()
    model._model = fake_model

    result = model.embed_texts(
        [
            "How do I apply?",
            "What is the eligibility criteria?",
        ]
    )

    assert result == [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    fake_model.embed.assert_called_once_with(
        documents=[
            "How do I apply?",
            "What is the eligibility criteria?",
        ],
        batch_size=256,
    )


def test_embed_texts_returns_empty_list_for_empty_input():
    model = EmbeddingModel()

    assert model.embed_texts([]) == []
    assert model._model is None


def test_embed_texts_rejects_whitespace_only_input():
    model = EmbeddingModel()

    with pytest.raises(ValueError, match="Input texts cannot contain empty"):
        model.embed_texts(["Valid text", "   "])

    assert model._model is None
