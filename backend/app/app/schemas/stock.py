import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class StockBase(BaseModel):
    ticker: str
    country: str
    url: Optional[str] = None
    desc: Optional[str] = None
    side: int = 1
    price: Optional[float] = None
    signal_id: int


# Properties to receive on item creation
class StockCreate(StockBase):
    pass


# Properties to receive on item update
class StockUpdate(StockBase):
    pass


# Properties shared by models stored in DB
class StockInDBBase(StockBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Stock(StockInDBBase):
    pass


# Properties properties stored in DB
class StockInDB(StockInDBBase):
    pass
