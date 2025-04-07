from .crud import users_repository, UsersRepository
from app.core.base.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from .model import UsersOrm
from sqlalchemy import func, select
from app.core.config import settings
import random


import logging

logger = logging.getLogger(__name__)


class UsersService(BaseService):
    def __init__(self, repository: UsersRepository):
        self.repository = repository
        super().__init__(repository=self.repository)


users_service: UsersService = UsersService(repository=users_repository)