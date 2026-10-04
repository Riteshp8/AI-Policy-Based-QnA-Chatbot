from functools import lru_cache

import numpy as np

from app.core.config import settings


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer  # lazy: slow import, downloads model on first use
    return SentenceTransformer(settings.embedding_model)


def embed(texts: list[str]) -> np.ndarray:
    return np.asarray(_model().encode(texts, normalize_embeddings=True, batch_size=32), dtype="float32")
