from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    emoji: Mapped[str] = mapped_column(String(8), default="🙂")
    tagline: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    personality: Mapped[list[str]] = mapped_column(JSON, default=list)
    greeting: Mapped[str] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
