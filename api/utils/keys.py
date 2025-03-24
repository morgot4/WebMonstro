from core.models.db_helper import db_helper
from sqlalchemy import insert
from core.models.keys import VideoKeywordsOrm

import asyncio
from fastapi import APIRouter

router = APIRouter(prefix="/setup")
