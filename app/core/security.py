from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_delta: timedelta) -> str:
    if not isinstance(subject, str):
        raise ValueError("JWT subject must be a string")
    to_encode: dict[str, str | datetime] = {"sub": subject}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"Decoded subject: {payload}")
        subject = payload.get("sub")
        if not isinstance(subject, str):
            raise JWTError("Token missing or invalid subject")
        return subject
    except JWTError as e:
        print(f"Token decode error: {str(e)}")
        raise JWTError(f"Invalid token: {str(e)}")
    
    
