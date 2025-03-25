from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import KeywordsOrm


async def get_random_row(
    session: AsyncSession, 
    min_words: int, 
    max_words: int,
    limit: int = 1
):
    subquery = (
        select(KeywordsOrm.id)
        .where(
            KeywordsOrm.words_count.between(min_words, max_words)
        )
        .order_by(func.random())
        .limit(limit)
    )
    
    # Основной запрос для получения полной информации о записях
    query = select(KeywordsOrm).where(
        KeywordsOrm.id.in_(subquery)
    )
    
    result = await session.execute(query)
    return result.scalar()