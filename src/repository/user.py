from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID

from src.model.user import User


def get_user_by_id(db: Session, user_id: UUID) -> Any:
    return db.query(User).filter_by(id=user_id).first()


def save_user_follow(db: Session, follower_id: UUID, followed_id: UUID) -> None:
    followed = get_user_by_id(db, followed_id)
    follower = get_user_by_id(db, follower_id)

    follower.following.append(followed)
    db.add(follower)
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
