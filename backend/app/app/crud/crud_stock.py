from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockUpdate


class CRUDStock(CRUDBase[Stock, StockCreate, StockUpdate]):

    def get_last(self, db: Session) -> Stock:
        return db.query(self.model).order_by(self.model.id.desc()).first()

    def get_multi_by_signal(
            self, db: Session, *, signal_id: int, skip: int = 0, limit: int = 100
    ) -> List[Stock]:
        return (
            db.query(self.model)
                .filter(Stock.signal_id == signal_id)
                .offset(skip)
                .limit(limit)
                .all()
        )


stock = CRUDStock(Stock)
