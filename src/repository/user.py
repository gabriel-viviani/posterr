from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID

from src.model.user import User, Follow


def get_user_by_id(db: Session, user_id: UUID) -> Any:
    return db.query(User).filter_by(id=user_id).first()


def get_user_following_num(db: Session, user_id: UUID) -> Any:
    return db.query(Follow).filter_by(follower_id=user_id).count()
