from typing import Optional

from pydantic import BaseModel

# Shared properties
from app.schemas.stock import Stock


class ItemBase(BaseModel):
    qty: float = 0


# Properties to receive on item creation
class ItemCreate(ItemBase):
    stock_id: int


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    owner_id: int
    stock_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    stock: Stock
    current_price: Optional[float]


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
