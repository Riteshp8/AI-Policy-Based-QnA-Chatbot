from app.core.config import settings
from app.services import embedding_service, vector_store


def retrieve(question: str) -> list[dict]:
    q = embedding_service.embed([question])[0]
    return [h for h in vector_store.search(q, settings.top_k) if h["score"] >= settings.min_score]
