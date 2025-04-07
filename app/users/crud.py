from app.core.base.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .model import UsersOrm
import logging


logger = logging.getLogger(__name__)

class UsersRepository(BaseRepository):
    model = UsersOrm

 
users_repository: UsersRepository = UsersRepository()

        