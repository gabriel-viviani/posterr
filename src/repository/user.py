from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID

from src.model.user import User, Follow


def get_user_by_id(db: Session, user_id: UUID) -> Any:
    return db.query(User).filter_by(id=user_id).first()


def get_user_following_num(db: Session, user_id: UUID) -> Any:
    return db.query(Follow).filter_by(follower_id=user_id).count()


def save_user_follow(db: Session, follow: Follow) -> None:
    db.add(follow)
    db.commit()


def get_follow_relation(db: Session, follower_id: UUID, following_id: UUID) -> Any:
    return (
        db.query(Follow)
        .filter_by(follower_id=follower_id, following_id=following_id)
        .all()
    )


def delete_user_follow(db: Session, follower_id: UUID, followed_id: UUID) -> None:
    db.query(Follow).filter_by(
        follower_id=follower_id, following_id=followed_id
    ).delete()
    db.commit()
