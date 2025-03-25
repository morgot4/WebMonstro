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

    def setup_keys(self):
        self.client.execute(
            """CREATE TABLE IF NOT EXIST keys (
                id UInt32,
                text String,
                frequency UInt32,
                words_count UInt8
            ) ENGINE = MergeTree()
            ORDER BY (words_count, id)
            """
        )
        


db_helper = DatabaseHelper(url=settings.DATABASE_URL_asyncpg, echo=False)
