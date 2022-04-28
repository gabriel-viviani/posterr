from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID

from src.config import generate_today
from src.model.post import Post
from src.model.user import User


def get_posts(db: Session, params: Params) -> Any:
    return paginate(
        db.query(Post)
        .filter(Post.author_id.in_([]))
        .order_by(Post.created_at.desc())
        .all(),
        params,
    )


def get_today_posts_by_author(db: Session, author_id: UUID) -> Any:
    return (
        db.query(Post).filter_by(author_id=author_id, created_at=generate_today()).all()
    )


def save_post(db: Session, post: Post) -> None:
    db.add(post)
    db.commit()


def get_post_by_id(db: Session, post_id: UUID) -> Any:
    return db.query(Post).filter_by(id=post_id).first()


def get_posts_by_author(db: Session, params: Params, author_id: UUID) -> Any:
    return paginate(db.query(Post).filter_by(author_id=author_id).all(), params)


def get_following_posts(db: Session, params: Params, user_id: str) -> Any:
    return paginate(
        db.query(Post)
        .join(User)
        .filter(User.id == user_id)
        .order_by(Post.created_at.desc())
        .all(),
        params,
    )
