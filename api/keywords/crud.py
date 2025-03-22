from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func
from sqlalchemy import select
from fastapi import Depends
from core.models.keys import VideoKeywordsOrm

async def get_random_video_keyword(session: AsyncSession) -> VideoKeywordsOrm:
    query = select(VideoKeywordsOrm).order_by(func.random()).limit(1)
    res = await session.execute(query)
    return res.scalar()