import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .signal import Signal  # noqa: F401


class Side(enum.Enum):
    buy = 1
    sell = 2


class Stock(Base):
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    country = Column(String, index=True)
    url = Column(String)
    desc = Column(String)
    side = Column(Integer)
    price = Column(Float)
    signal_id = Column(Integer, ForeignKey("signal.id"))
    signal = relationship("Signal", back_populates="stocks")
    item = relationship("Item", back_populates="stock")
