from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import admin_only, current_user
from app.database.database import SessionLocal, get_db
from app.models.policy import Policy
from app.services import embedding_service, pdf_processor, vector_store

router = APIRouter()
MAX_BYTES = 20 * 1024 * 1024


def _out(p: Policy) -> dict:
    return {"id": p.id, "name": p.name, "date": p.uploaded_at.isoformat(), "status": p.status, "pages": p.pages}


def index_policy(policy_id: int) -> None:
    """Background task: PDF -> chunks -> embeddings -> vector store."""
    db = SessionLocal()
    p = db.get(Policy, policy_id)
    try:
        chunks, pages = pdf_processor.extract_chunks(settings.policies_dir / p.filename)
        if not chunks:
            raise ValueError("No extractable text (scanned PDF?)")
        vector_store.add_policy(p.id, p.name, chunks, embedding_service.embed([c["text"] for c in chunks]))
        p.pages, p.status = pages, "Active"
    except Exception:
        p.status = "Failed"
    db.commit()
    db.close()


@router.get("")
def list_policies(db: Session = Depends(get_db), _=Depends(current_user)):
    return [_out(p) for p in db.query(Policy).order_by(Policy.uploaded_at.desc())]


@router.post("/upload", status_code=201)
async def upload(background: BackgroundTasks, file: UploadFile = File(...),
                 db: Session = Depends(get_db), _=Depends(admin_only)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "File too large (max 20 MB)")
    p = Policy(name=Path(file.filename).stem, status="Processing")
    db.add(p); db.commit(); db.refresh(p)
    settings.policies_dir.mkdir(parents=True, exist_ok=True)
    path = settings.policies_dir / f"{p.id}.pdf"
    path.write_bytes(data)
    p.filename = path.name
    db.commit()
    background.add_task(index_policy, p.id)
    return _out(p)


@router.delete("/{policy_id}", status_code=204)
def delete_policy(policy_id: int, db: Session = Depends(get_db), _=Depends(admin_only)):
    p = db.get(Policy, policy_id)
    if not p:
        raise HTTPException(404, "Policy not found")
    (settings.policies_dir / f"{p.id}.pdf").unlink(missing_ok=True)
    vector_store.delete_policy(p.id)
    db.delete(p)
    db.commit()
