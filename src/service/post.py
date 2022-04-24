from sqlalchemy.orm import Session
from typing import List, Optional

from src.dto.post import PostDto, CreatePost, CreateQuote, CreateRepost
from src.repository.post import get_posts, get_following_posts
from src.model.post import Post
from src.dto.user import UserDto


def get_posts(
    db: Session, limit: int, only_follower: bool, user_id
) -> Optional[List[PostDto]]:
    if only_follower:
        posts = get_following_posts(db, limit, user_id)

        if not posts:
            return []

        return [
            PostDto(
                id=post.id,
                text=post.text,
                created_at=post.created_at,
                user=UserDto(id=post.user.id, username=post.user.username),
            )
            for post in posts
        ]

    posts = get_posts(db, limit)
    if not posts:
        return []

    return [
        PostDto(
            id=post.id,
            text=post.text,
            created_at=post.created_at,
            user=UserDto(id=post.user.id, username=post.user.username),
        )
        for post in posts
    ]


def create_post(db: Session, new_post: CreatePost) -> None:
    post = Post()
