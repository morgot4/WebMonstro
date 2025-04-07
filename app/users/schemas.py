from pydantic import BaseModel, ConfigDict
import datetime


class BaseUser(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseUser):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(BaseUser):
    pass

class UserFilter(BaseModel): #for filters 
    id: int | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None    
    username: str | None = None
    email: str | None = None
    password: str | None = None