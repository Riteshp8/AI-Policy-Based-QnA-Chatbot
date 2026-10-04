# AI Policy QnA Chatbot (PolicyMind)

RAG chatbot that answers questions from uploaded policy PDFs and cites document, section and page.

## Run
```bash
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 (frontend is served by FastAPI). API docs: http://127.0.0.1:8000/docs

## Config (`backend/.env`)
- `SECRET_KEY`: JWT signing key. Change it.
- `ADMIN_EMAILS`: emails that become Admin on signup.
- `GEMINI_API_KEY`: optional. Empty = returns the best-matching policy text without an LLM.

## How it works
Upload PDF (admin) -> `pdf_processor` chunks by page/section -> `embedding_service` (MiniLM) -> `vector_store` (`/vectorstore`).
Question -> `retrieval_service` (top-k, min score) -> `chatbot_service` (LLM answers only from context) -> answer + sources, or "not found".

## Frontend status
`frontend/` is plain HTML/CSS/JS (no build step) and currently runs on mock data in `services/api.js`.
The `api.*` client there already matches the backend routes; switch pages from mock to `api.*` to go live.

## Tests
```bash
cd backend && pytest ../tests
```
