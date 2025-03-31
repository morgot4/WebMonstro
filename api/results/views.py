from fastapi import APIRouter, Query, HTTPException, status, Body, Header, Depends
from fastapi.responses import FileResponse
from .schemas import ClickResult
from .utils import generate_click_result, click_result_by_id, click_result_by_keyword, click_result_by_domain, click_result_by_party, click_result_by_profile_id
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/results", tags=["Results"])

@router.get("/upload/", response_model=ClickResult)
async def get_info_from_monstro(click_result = Depends(generate_click_result), session: AsyncSession = Depends(db_helper.session_dependency)):
   return click_result

   

@router.get("")
async def get_results(session: AsyncSession = Depends(db_helper.session_dependency)):
    pass

@router.get("/{keyword}", response_model=list[ClickResult])
async def get_result_by_keyword(results: list[ClickResult] = Depends(click_result_by_keyword)) -> list[ClickResult]:
    return results

@router.get("/{click_result_id}", response_model=ClickResult)
async def get_result_by_id(result: ClickResult = Depends(click_result_by_id)) -> ClickResult:
    return result

@router.get("/{domain}", response_model=list[ClickResult])
async def get_result_by_keyword(results: list[ClickResult] = Depends(click_result_by_domain)) -> list[ClickResult]:
    return results

@router.get("/{party}", response_model=list[ClickResult])
async def get_result_by_party(results: list[ClickResult] = Depends(click_result_by_party)) -> list[ClickResult]:
    return results

@router.get("/{profile_id}", response_model=list[ClickResult])
async def get_result_by_profile_id(results: list[ClickResult] = Depends(click_result_by_profile_id), session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ClickResult]:
    return results