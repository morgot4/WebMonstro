from fastapi import APIRouter, Query, HTTPException, status, Body, Header, Depends
from fastapi.responses import FileResponse, HTMLResponse
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import *

router = APIRouter(prefix="/keywords", tags=["Keywords"])


@router.get("/video")
async def rand_video_keyword(session: AsyncSession = Depends(db_helper.session_dependency)):
    res = await get_random_video_keyword(session=session)
    return HTMLResponse(res.text)