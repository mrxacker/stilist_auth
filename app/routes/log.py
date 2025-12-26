from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.log import LogRequest
from app.repository import log as log_repo
from app.core.security import decode_access_token
from jose import JWTError


router = APIRouter(prefix="/log", tags=["Log"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", status_code=201)
def register(data: LogRequest, db: Session = Depends(get_db)):
    token = data.access_token
    try:
        user_id = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
        
    if int(user_id) != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID does not match token",
        )
    
    log_repo.create(db, data.user_id, data.action, data.timestamp)
    return {"message": "Log created"}
