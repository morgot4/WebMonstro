from .schemas import ProfileRead
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Path
from core.models import db_helper
from .crud import *
from typing import Annotated

async def profile_by_pid(pid: Annotated[int, Path] , session: AsyncSession = Depends(db_helper.session_dependency)) -> ProfileRead:
    return await get_profile_by_pid(pid=pid, session=session)

async def profiles_by_party(party: Annotated[str, Path], session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ProfileRead]:
    return await get_profiles_by_party(party=party, session=session)

