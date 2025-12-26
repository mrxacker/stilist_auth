from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password


def get_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create(db: Session, username: str, password: str) -> User:
    user = User(
        username=username,
        password_hash=hash_password(password),
        active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: int) -> User | None:
    user = get_by_id(db, user_id)
    if user:
        user.active = False
        db.commit()
        db.refresh(user)
    return user