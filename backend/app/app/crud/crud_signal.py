from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.signal import Signal
from app.schemas.signal import SignalCreate, SignalUpdate


class CRUDSignal(CRUDBase[Signal, SignalCreate, SignalUpdate]):

    def get_last(self, db: Session) -> Signal:
        return db.query(self.model).order_by(self.model.id.desc()).first()


signal = CRUDSignal(Signal)
