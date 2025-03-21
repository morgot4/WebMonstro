from pydantic import BaseModel
import datetime


class ClickResult(BaseModel):
    find: bool
    clickurl: bool
    error: bool
    pos: int
    copyname: str
    profile_id: int
    data_create: datetime.datetime
    yacount: int
    metrikacount: int
    search_type: str
    search_domain: str
    domain: str
    party: str
    keyword: str
    lendomain: int
    lencookies: int
