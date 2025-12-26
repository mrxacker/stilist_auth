from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.log import LogRequest, LogResponse
from app.repository import log as log_repo
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/log", tags=["Log"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", status_code=201)
def register(data: LogRequest, db: Session = Depends(get_db)):
    log_repo.create(db, data.user_id, data.action, data.timestamp)
    return {"message": "Log created"}
