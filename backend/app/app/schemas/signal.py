import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class SignalBase(BaseModel):
    created_datetime: Optional[datetime.datetime] = None
    text: Optional[str] = None


# Properties to receive on item creation
class SignalCreate(SignalBase):
    pass


# Properties to receive on item update
class SignalUpdate(SignalBase):
    pass


# Properties shared by models stored in DB
class SignalInDBBase(SignalBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Signal(SignalInDBBase):
    pass


# Properties properties stored in DB
class SignalInDB(SignalInDBBase):
    pass
