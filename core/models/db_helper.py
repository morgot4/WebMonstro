from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from core.config import settings
from asyncio import current_task
import logging
import asyncio
from aiochclient import ChClient
from aiohttp import ClientSession
from typing import Optional
from collections import deque
logger = logging.getLogger('my_app')

class AsyncClickHouse:
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
        self._session = None
        self._client = None

    async def __aenter__(self):
        self._session = ClientSession()
        self._client = ChClient(
            self._session,
            url=f"https://{self.host}:8443",
            user=self.user,
            password=self.password,
            json=True
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._session.close()

    async def get_random_text(self, min_words: int, max_words: int) -> Optional[str]:
        
        query = """
        SELECT text
        FROM keywords
        WHERE words_count BETWEEN {min_words} AND {max_words}
        ORDER BY rand()
        LIMIT 1
        """
        return await self._client.fetchval(query, params={
                'min_words': min_words,
                'max_words': max_words
            })
    


class RandomTextPool:
    def __init__(self, host: str, user: str, password: str, pool_size: int = 10):
        self.host = host
        self.user = user
        self.password = password
        self.pool_size = pool_size
        self.pool = deque()
        self.refill_lock = asyncio.Lock()
        
    async def _fetch_random_text(self, min_words: int, max_words: int) -> str:
        query = """
        SELECT text FROM keywords 
        WHERE words_count BETWEEN {min} AND {max}
        ORDER BY rand() LIMIT 1
        """
        async with ClientSession() as session:
            client = ChClient(session, url=f"https://{self.host}:8443", 
                            user=self.user, password=self.password)
            return await client.fetchval(query, params={'min': min_words, 'max': max_words})

    async def _refill_pool(self, min_words: int, max_words: int):
        async with self.refill_lock:
            while len(self.pool) < self.pool_size:
                
                task = asyncio.create_task(
                    self._fetch_random_text(min_words, max_words)
                )
                self.pool.append(task)

    async def get_text(self, min_words: int, max_words: int) -> str:
        """Получает текст из пула или инициирует фоновую подгрузку"""
        if not self.pool:
            logger.info("The pool is empty. Try to get from clickhouse")
            # Если пул пуст - ждем один результат
            res = await self._fetch_random_text(min_words, max_words)
            task = asyncio.create_task(
                    self._fetch_random_text(min_words, max_words)
                )
            self.pool.append(task)
            #logger.info(f"Created and added a new task to pool, pool size: {len(self.pool)}")
            return res
        
        # Забираем первый доступный результат
        task = self.pool.popleft()
        #logger.info(f"Get text from pool, pool size: {len(self.pool)}")
        
        # Запускаем фоновое пополнение пула
        asyncio.create_task(self._refill_pool(min_words, max_words))
        
        return await task
    



class DatabaseHelper:

    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()



db_helper = DatabaseHelper(url=settings.DATABASE_URL_asyncpg, echo=False)
clickhouse_helper =  AsyncClickHouse(host=settings.CLICKHOUSE_HOST, user=settings.CLICKHOUSE_USERNAME, password=settings.CLICKHOUSE_PASSWORD)
keywords_pool = RandomTextPool(host=settings.CLICKHOUSE_HOST, user=settings.CLICKHOUSE_USERNAME, password=settings.CLICKHOUSE_PASSWORD)