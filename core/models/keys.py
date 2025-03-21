from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from typing import Annotated
from sqlalchemy import text
from .base import Base


class KeysOrm(Base):
    __tablename__ = "info_keys"

    text: Mapped[str] = mapped_column(nullable=True)
