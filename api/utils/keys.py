from core.models.db_helper import db_helper
from sqlalchemy import insert
from core.models.keys import KeysOrm

import asyncio
from fastapi import APIRouter

router = APIRouter(prefix="/setup")


async def setup_keys(data, session=db_helper.get_scoped_session()):
    for i, key in enumerate(data):
        session.add(KeysOrm(id=i, text=key))
        await session.commit()
    await session.close()
