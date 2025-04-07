from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import *
from .service import users_service
from app.core.session_manager import SessionDep
import random

router = APIRouter(prefix="/keywords", tags=["Keywords"])


@router.get("/{id}")
async def get_users_by_id(id, session: AsyncSession = SessionDep):
    res = await users_service.find_one_or_none_by_pid(session=session, data_pid=id)
    return res
