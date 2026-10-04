from app.core.config import settings
from app.services import retrieval_service

NOT_FOUND = "I couldn't find this information in the available policy documents."
SYSTEM = (
    "You answer questions about company policies using ONLY the provided context. "
    "Be concise and accurate. If the context does not contain the answer, reply with exactly NOT_FOUND."
)


def _llm(question: str, hits: list[dict]) -> str:
    from google import genai
    ctx = "\n\n".join(f"[{h['document']} | {h['section']} | p.{h['page']}]\n{h['text']}" for h in hits)
    r = genai.Client(api_key=settings.gemini_api_key).models.generate_content(
        model=settings.llm_model,
        contents=f"Context:\n{ctx}\n\nQuestion: {question}",
        config={"system_instruction": SYSTEM, "max_output_tokens": 500},
    )
    return (r.text or "NOT_FOUND").strip()


def answer(question: str) -> dict:
    hits = retrieval_service.retrieve(question)
    text = (_llm(question, hits) if settings.gemini_api_key else hits[0]["text"]) if hits else "NOT_FOUND"
    if text == "NOT_FOUND":
        return {"found": False, "answer": NOT_FOUND, "sources": []}
    sources = [{"document": h["document"], "section": h["section"], "page": h["page"],
                "score": round(min(h["score"], 1) * 100)} for h in hits[:3]]
    return {"found": True, "answer": text, "sources": sources}
