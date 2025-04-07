from sqlalchemy.orm import mapped_column, Mapped
from app.core.base.base_model import Base, idpk


class UsersOrm(Base):
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    #Just example of model