from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func
from sqlalchemy import select
from fastapi import Depends
from .utils import get_random_row
from core.models.keys import VideoKeywordsOrm, KeywordsOrm
import random

async def get_random_video_keyword(session: AsyncSession) -> VideoKeywordsOrm:
    return await session.get(VideoKeywordsOrm, random.randint(1, 19 * 10**3))


async def get_random_keyword(min_count, max_count, session: AsyncSession) -> KeywordsOrm:
    return await get_random_row(session=session, min_words=min_count, max_words=max_count)
    