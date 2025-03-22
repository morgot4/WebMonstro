from pydantic import BaseModel
import datetime


class Keyword(BaseModel):
    text: str
    frequecy: int