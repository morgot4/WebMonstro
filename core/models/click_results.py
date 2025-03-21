from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from typing import Annotated
from sqlalchemy import text, ForeignKey
from .base import Base
import datetime


class ClickResultsOrm(Base):
    __tablename__ = "results"

    find: Mapped[bool]
    clickurl: Mapped[bool]
    error: Mapped[bool]
    pos: Mapped[int]
    copyname: Mapped[str]
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.profile_id"))
    data_create: Mapped[datetime.datetime]
    yacount: Mapped[int]
    metrikacount: Mapped[int]
    search_type:  Mapped[str]
    search_domain: Mapped[str]
    domain: Mapped[str]
    party: Mapped[str]
    ask: Mapped[str]
    lendomain: Mapped[int]
    lencookies: Mapped[int]
