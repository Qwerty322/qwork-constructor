from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .stock import Stock  # noqa: F401


class Signal(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_datetime = Column(DateTime)
    text = Column(String)
    stocks = relationship("Stock", back_populates="signal")
