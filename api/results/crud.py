from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends
from core.models.click_results import ClickResultsOrm
from core.models import db_helper


async def get_click_result_by_id(click_result_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> ClickResultsOrm:
    return await session.get(ClickResultsOrm, click_result_id)


async def get_click_results_by_keyword(keyword: str, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResultsOrm]:
    query = select(ClickResultsOrm).where(ClickResultsOrm.ask == keyword)
    res = await session.execute(query)
    return res.scalars().all()


async def get_click_results_by_domain(domain: str, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResultsOrm]:
    query = select(ClickResultsOrm).where(ClickResultsOrm.domain == domain)
    res = await session.execute(query)
    return res.scalars().all()


async def get_click_results_by_party(party: str, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResultsOrm]:
    query = select(ClickResultsOrm).where(ClickResultsOrm.party == party)
    res = await session.execute(query)
    return res.scalars().all()


async def get_click_results_by_profile_id(profile_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResultsOrm]:
    query = select(ClickResultsOrm).where(ClickResultsOrm.profile_id == profile_id)
    res = await session.execute(query)
    return res.scalars().all()

