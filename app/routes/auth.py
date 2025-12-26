from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.repository import user as user_repo
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if data.admin_code:
        if data.admin_code != settings.ADMIN_PASSWORD:
            raise HTTPException(status_code=400, detail="Invalid admin code")
    else:
        if data.admin_code is not None:
            raise HTTPException(status_code=400, detail="Admin code required for admin registration")

    if user_repo.get_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="User already exists")

    user_repo.create(db, data.username, data.password)
    return {"message": "User registered"}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = user_repo.get_by_username(db, data.username)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": token}
