from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker
from core.config import settings
from asyncio import current_task
import clickhouse_driver


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


class ClickHouseHelper:
    def __init__(self, host, username, password):
        self.client = clickhouse_driver.Client(host=host, user=username, password=password, secure=True, verify=True)


    def get_random_text(self, min_words: int, max_words: int) -> str:
        """
        Выбирает случайный текст с заданным диапазоном длины слов
        
        Параметры:
            min_words: минимальное количество слов
            max_words: максимальное количество слов
            host: хост ClickHouse
            user: пользователь
            password: пароль
        
        Возвращает:
            Случайный текст или None, если не найдено
        """

        try:
            # 1. Быстрая проверка наличия данных
            count = self.client.execute(
                "SELECT count() FROM keywords "
                "WHERE words_count BETWEEN %(min)s AND %(max)s",
                {'min': min_words, 'max': max_words}
            )[0][0]
            
            if count == 0:
                return None
            
            # 2. Оптимизированный запрос с использованием материализованного представления
            query = """
            SELECT text
            FROM keywords
            WHERE words_count BETWEEN %(min)s AND %(max)s
            ORDER BY rand()
            LIMIT 1
            """
            
            return self.client.execute(query, {'min': min_words, 'max': max_words})[0][0]
        
        finally:
            self.client.disconnect()



db_helper = DatabaseHelper(url=settings.DATABASE_URL_asyncpg, echo=False)
clickhouse_helper = ClickHouseHelper(host=settings.CLICKHOUSE_HOST, username=settings.CLICKHOUSE_USERNAME, password=settings.CLICKHOUSE_PASSWORD)