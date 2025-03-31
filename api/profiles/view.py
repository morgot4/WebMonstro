from fastapi import APIRouter, Query, HTTPException, status, Body, Header, Depends
from fastapi.responses import FileResponse
from .schemas import ProfileRead, SelectionParameter
from .utils import profile_by_pid, profiles_by_party
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import *



router = APIRouter(prefix="/profiles", tags=["Profiles"])



@router.get("/pid/{pid}", response_model=ProfileRead)
async def get_profile_by_pid(result: ProfileRead = Depends(profile_by_pid)) -> ProfileRead:
    return result

@router.get("/party/{party}", response_model=list[ProfileRead])
async def get_profiles_by_party(results: list[ProfileRead] = Depends(profiles_by_party)) -> list[ProfileRead]:
    return results

@router.post("/selection")
async def profiles_selection(select_model: SelectionParameter, session: AsyncSession = Depends(db_helper.session_dependency)):
    count = await setup_profiles_by_parameters(session=session, **select_model.model_dump())
    return {"success": True, "count": count}