from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.security import current_user
from app.database.database import get_db
from app.models.chat_history import Chat, Message
from app.models.user import User
from app.services import chatbot_service

router = APIRouter()


class AskIn(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    chat_id: int | None = None


def _chat(c: Chat) -> dict:
    return {"id": c.id, "title": c.title, "date": c.created_at.isoformat(),
            "messages": [{"role": m.role, "text": m.text, "found": m.found, "sources": m.sources or []} for m in c.messages]}


@router.post("/ask")
def ask(b: AskIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    chat = None
    if b.chat_id:
        chat = db.get(Chat, b.chat_id)
        if not chat or chat.user_id != user.id:
            raise HTTPException(404, "Chat not found")
    if not chat:
        chat = Chat(user_id=user.id, title=b.question[:80])
        db.add(chat)
        db.flush()
    result = chatbot_service.answer(b.question)
    db.add(Message(chat_id=chat.id, role="user", text=b.question, found=True, sources=[]))
    db.add(Message(chat_id=chat.id, role="assistant", text=result["answer"], found=result["found"], sources=result["sources"]))
    db.commit()
    db.refresh(chat)
    return _chat(chat)


@router.get("")
def list_chats(db: Session = Depends(get_db), user: User = Depends(current_user)):
    return [_chat(c) for c in db.query(Chat).filter_by(user_id=user.id).order_by(Chat.created_at.desc())]


@router.delete("/{chat_id}", status_code=204)
def delete_chat(chat_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    c = db.get(Chat, chat_id)
    if not c or c.user_id != user.id:
        raise HTTPException(404, "Chat not found")
    db.delete(c)
    db.commit()
