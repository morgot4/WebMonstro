__all__ = ("monstro",)

from fastapi import APIRouter
from .task.views import router as tasks_router
from .results.views import router as results_router
from .keywords.view import router as keywords_router
from .profiles.view import router as profiles_router
from .monstro_settings.view import router as monstro_settings_router

monstro = APIRouter(prefix="/monstro")
monstro.include_router(router=tasks_router)
monstro.include_router(router=results_router)
monstro.include_router(router=keywords_router)
monstro.include_router(router=profiles_router)
monstro.include_router(router=monstro_settings_router)