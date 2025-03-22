from fastapi import APIRouter, Query, HTTPException, status, Body, Header, Depends
from fastapi.responses import FileResponse
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import *

router = APIRouter(prefix="/keywords", tags=["Keywords"])


@router.get("/video", response_model=str)
async def rand_video_keyword(session: AsyncSession = Depends(db_helper.session_dependency)):
    res = await get_random_video_keyword(session=session)
    return res.text