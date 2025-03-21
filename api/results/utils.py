from .schemas import ClickResult
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.models import db_helper
from .crud import *

async def generate_click_result(
    find,
    clickurl,
    error,
    pos,
    copyname,
    profileid,
    data_create,
    yacount,
    metrikacount,
    search_type,
    search_domain,
    domain,
    party,
    ask,
    lendomain,
    lencookies,
):
    return ClickResult(
        find,
        clickurl,
        error,
        pos,
        copyname,
        profileid,
        data_create,
        yacount,
        metrikacount,
        search_type,
        search_domain,
        domain,
        party,
        ask,
        lendomain,
        lencookies,
    )


async def click_result_by_id(click_result_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> ClickResult:
    return await get_click_result_by_id(click_result_id=click_result_id, session=session)


async def click_result_by_keyword(keyword: str, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResult]:
    return await get_click_results_by_keyword(keyword=keyword, session=session)


async def click_result_by_domain(domain: str, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResult]:
    return await get_click_results_by_domain(domain=domain, session=session)

async def click_result_by_party(party: str, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResult]:
    return await get_click_results_by_party(party=party, session=session)

async def click_result_by_profile_id(profile_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResult]:
    return await get_click_results_by_profile_id(profile_id=profile_id, session=session)