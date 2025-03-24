from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from typing import Annotated
from sqlalchemy import text
from .base import Base, idpk


class VideoKeywordsOrm(Base):
    __tablename__ = "video_keys"
    id: Mapped[idpk]
    text: Mapped[str] = mapped_column(nullable=True)
    frequency: Mapped[int]
