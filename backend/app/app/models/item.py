from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .stock import Stock  # noqa: F401


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
    stock_id = Column(Integer, ForeignKey("stock.id"))
    stock = relationship("Stock", back_populates="item")
    qty = Column(Float)
