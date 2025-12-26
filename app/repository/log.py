from sqlalchemy.orm import Session

from app.models.user import User, Log
from app.core.security import hash_password


def get_log_by_user_id(db: Session, user_id: int) -> list[Log] | None:
    return db.query(Log).filter(Log.user_id == user_id).all()


def create(db: Session, user_id: int, action: str, timestamp: str) -> Log:
    log = Log(
        user_id=user_id,
        action=action,
        timestamp=timestamp
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
