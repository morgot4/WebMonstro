from .crud import click_result_repository, ClickResultsRepository
from .schemas import ClickResult
from app.core.base.base_service import BaseService


class ClickResultService(BaseService):
    def __init__(self, repository):
        super().__init__(repository=repository)
        

    
click_result_service: ClickResultService = ClickResultService(repository=click_result_repository)