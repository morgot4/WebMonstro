from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from typing import Annotated
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import text
import datetime

idpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    TIMESTAMP(timezone=True), mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    TIMESTAMP(timezone=True),
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    ),
]


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[idpk]
