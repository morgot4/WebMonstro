from fastapi import APIRouter, Query, HTTPException, status, Body, Header, Depends
from fastapi.responses import FileResponse, HTMLResponse
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
import random



router = APIRouter(prefix="/settings", tags=["Keywords"])

@router.get("/stream")
async def get_stream():
    return random.randint(1, 3)


@router.get("/query")
async def get_stream():
    return random.randint(1, 3)


@router.get("/count")
async def get_stream():
    return random.randint(40, 50)