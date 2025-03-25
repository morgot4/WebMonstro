from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func
from sqlalchemy import select
from fastapi import Depends
from core.models.db_helper import clickhouse_helper, keywords_pool
from core.models.keys import VideoKeywordsOrm, KeywordsOrm
import random
from core.config import settings
import logging

logger = logging.getLogger("my_app")

async def get_random_video_keyword(session: AsyncSession) -> VideoKeywordsOrm:
    return await session.get(VideoKeywordsOrm, random.randint(1, 19 * 10**3))


async def get_random_keyword(pid, min_count, max_count) -> KeywordsOrm:
    res = await keywords_pool.get_text(min_count, max_count)
    logger.info(f"Profile: {pid}. Get random keyword: {res}")
    return res
        