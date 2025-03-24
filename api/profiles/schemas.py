from pydantic import BaseModel
import datetime



class ProfileRead(BaseModel):
    pid: int
    data_create: datetime.datetime
    party: str	
    cookies_len: int	
    accounts: str	
    is_google: bool
    is_yandex: bool
    is_mail: bool
    is_youtube: bool
    ismobiledevice: bool	
    platform: str		
    platform_version: str		
    browser: str		
    browser_version: str	
    folder: str		
    fingerprints: str	
    cookies: str		
    localstorage: str		
    proxy: str
    last_date_work: datetime.datetime
    date_block: datetime.datetime
    last_visit_sites: str
    last_task: str
    geo: str
    tel: str
    email: str
    name: str
    mouse_config: str	
    domaincount: int
    metrikacount: int
    yacount: int
    warm: datetime.datetime


class ProfileUpdatePartial(BaseModel):
    party: str | None = None
    folder: str | None = None
    last_visit_sites: str
    last_task: str
    geo: str
    tel: str
    email: str
    name: str
    mouse_config: str
    
    
class SelectionParameter(BaseModel):
    parties: list[str]
    profiles_count: int
    min_len_folder: int 
    max_len_folder: int 
    min_age: int  #hours
    max_age: int #hours