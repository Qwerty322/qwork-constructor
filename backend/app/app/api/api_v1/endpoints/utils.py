from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr

from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.api import deps
from app.core.celery_app import celery_app
from app.schemas.stock import Stock
from app.utils import send_test_email

router = APIRouter()


@router.get("/test-invest/", response_model=List[Stock], status_code=200)
def test_invest(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Test invest results.
    """
    signal = crud.signal.get_last(db)
    if not signal:
        raise HTTPException(status_code=404, detail="Stocks not found")
    return signal.stocks


@router.post("/test-invest/", response_model=schemas.Msg, status_code=201)
def test_invest(
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test invest by worker.
    """
    celery_app.send_task("app.worker.invest_task")
    return {"msg": "Word received"}


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
        msg: schemas.Msg,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
        email_to: EmailStr,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


@router.get("/test-notification/", response_model=schemas.Msg, status_code=200)
def test_notification(
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test notifications.
    """
    celery_app.send_task("app.worker.notification_task")
    return {"msg": "Test email sent"}
