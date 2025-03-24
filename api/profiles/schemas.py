from pydantic import BaseModel
import datetime



class ProfileRead(BaseModel):
    pid: int
    data_create: datetime.datetime
    party: str | None	
    cookies_len: int | None	
    accounts: str | None	
    is_google: bool
    is_yandex: bool
    is_mail: bool
    is_youtube: bool
    ismobiledevice: bool	
    platform: str | None		
    platform_version: str | None		
    browser: str | None		
    browser_version: str | None	
    folder: str | None		
    fingerprints: str | None	
    cookies: str | None		
    localstorage: str | None		
    proxy: str | None
    last_date_work: datetime.datetime | None
    date_block: datetime.datetime | None
    last_visit_sites: str | None
    last_task: str | None
    geo: str | None 
    tel: str | None 
    email: str | None 
    name: str | None
    mouse_config: str | None	
    domaincount: int
    metrikacount: int | None
    yacount: int | None
    warm: datetime.datetime | None


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
    new_party: str
    profiles_count: int
    min_len_folder: int 
    max_len_folder: int 
    min_age: int  #hours
    max_age: int #hours