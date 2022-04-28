from fastapi import HTTPException, status
from fastapi_pagination import Params
from typing import List, Optional, Any
from sqlalchemy.orm import Session
from uuid import UUID

from src.dto.post import PostDto, CreatePost, CreateQuote, CreateRepost
from src.repository import post as post_repo
from src.service import user as user_service
from src.dto.user import UserDto
from src.model.post import Post


def get_posts(
    db: Session, params: Params, only_follower: bool, user_id: UUID
) -> Optional[List[PostDto]]:
    if only_follower:
        posts = post_repo.get_following_posts(db, params, user_id)

        if not posts:
            return []

        return _post_list_to_dto(posts)

    posts = post_repo.get_posts(db, params)
    if not posts:
        return []

    return _post_list_to_dto(posts)


def create_repost(db: Session, new_repost: CreateRepost) -> None:
    if (
        user_service.get_user(db, new_repost.author_id)
        and _referenced_post_exists(db, new_repost.referred_post_id)
        and _can_user_post(db, new_repost.author_id)
    ):
        post = Post(
            author_id=new_repost.author_id,
            type=new_repost.type,
            refered_post_id=new_repost.referred_post_id,
        )
        post_repo.save_post(post)

    return


def create_quote(db: Session, new_quote: CreateQuote) -> None:
    if (
        user_service.get_user(db, new_quote.author_id)
        and _referenced_post_exists(db, new_quote.referred_post_id)
        and _can_user_post(db, new_quote.author_id)
    ):
        post = Post(
            author_id=new_quote.author_id,
            text=new_quote.quote_text,
            type=new_quote.type,
            refered_post_id=new_quote.referred_post_id,
        )
        post_repo.save_post(post)

    return


def create_post(db: Session, new_post: CreatePost) -> None:
    if user_service.get_user(db, new_post.author_id) and _can_user_post(
        db, new_post.author_id
    ):
        post = Post(text=new_post.text, author_id=new_post.author_id)
        post_repo.save_post(db, post)

    return


def _can_user_post(db: Session, author_id: UUID) -> bool:
    existing_posts = post_repo.get_today_posts_by_author(db, author_id)
    if len(existing_posts) > 5:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Author with id {author_id} cannot post anymore today.",
        )

    return True


def _referenced_post_exists(db: Session, referred_post_id: UUID) -> bool:
    referred_post = post_repo.get_post_by_id(db, referred_post_id)
    if not referred_post:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Post {referred_post_id} does not exist.",
        )

    return True


def get_posts_by_author_id(
    db: Session, params: Params, author_id: UUID
) -> List[PostDto]:
    posts = post_repo.get_posts_by_author(db, params, author_id)
    return _post_list_to_dto(posts)


def _post_list_to_dto(posts: Any) -> List[PostDto]:
    [
        PostDto(
            id=post.id,
            text=post.text,
            created_at=post.created_at,
            type=post.type,
            user=UserDto(id=post.user.id, username=post.user.username),
        )
        for post in posts
    ]
