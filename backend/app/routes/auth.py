from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_token, current_user, hash_password, verify_password
from app.database.database import get_db
from app.models.user import User

router = APIRouter()


class SignupIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)


def _out(u: User) -> dict:
    return {"name": u.name, "email": u.email, "role": u.role}


@router.post("/signup", status_code=201)
def signup(b: SignupIn, db: Session = Depends(get_db)):
    email = b.email.lower()
    if db.query(User).filter_by(email=email).first():
        raise HTTPException(409, "Email already registered")
    role = "Admin" if email in [e.lower() for e in settings.admin_emails] else "User"
    u = User(name=b.name, email=email, password_hash=hash_password(b.password), role=role)
    db.add(u); db.commit(); db.refresh(u)
    return {"access_token": create_token(u), "user": _out(u)}


@router.post("/login")
def login(b: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter_by(email=b.email.lower()).first()
    if not u or not verify_password(b.password, u.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_token(u), "user": _out(u)}


@router.get("/me")
def me(u: User = Depends(current_user)):
    return _out(u)
