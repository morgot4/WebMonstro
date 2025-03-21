__all__ = ("monstro",)

from fastapi import APIRouter
from .task.views import router as tasks_router
from .results.views import router as results_router

monstro = APIRouter(prefix="/monstro")
monstro.include_router(router=tasks_router)
monstro.include_router(router=results_router)
