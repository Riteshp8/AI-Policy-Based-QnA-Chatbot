from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Policy(Base):
    __tablename__ = "policies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    filename: Mapped[str] = mapped_column(String(255), default="")
    pages: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(20), default="Processing")  # Processing | Active | Failed
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
