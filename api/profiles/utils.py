from .schemas import ProfileRead
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.models import db_helper
from .crud import *

async def profile_by_pid(pid: int, session: AsyncSession) -> ProfileRead:
    return await get_profile_by_pid(pid=pid, session=session)

async def profiles_by_party(party: str, session: AsyncSession) -> list[ProfileRead]:
    return await get_profiles_by_party(party=party, session=session)

