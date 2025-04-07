from app.core.base.base_repository import BaseRepository
from .model import ClickResultsOrm
import logging


logger = logging.getLogger(__name__)

class ClickResultsRepository(BaseRepository):
    model = ClickResultsOrm


click_result_repository: ClickResultsRepository = ClickResultsRepository()