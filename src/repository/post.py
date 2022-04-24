from sqlalchemy.orm import Session
from typing import Any

from src.model.post import Post
from src.model.user import User 


def get_posts(db: Session, limit: int) -> Any:
    return db.query(Post).filter(Post.author_id.in_([])).limit(limit).order_by(Post.created_at.desc()).all()

def get_following_posts(db: Session, limit: int, user_id: str) -> Any:
    return db.query(Post).join(User).filter(User.followers.any(User.id = user_id)).order_by(Post.created_at.desc()).limit(limit).all()
