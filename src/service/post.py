from typing import List, Optional, Any, Union
from fastapi import HTTPException, status
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from uuid import UUID

from src.dto.post import (
    PostDto,
    CreatePost,
    CreateQuote,
    CreateRepost,
    QuotePostDto,
    RepostDto,
    PostTypes,
)
from src.repository import post as post_repo
from src.service import user as user_service
from src.dto.user import UserDto
from src.model.post import Post


def get_posts(
    db: Session, params: Params, only_follower: bool, user_id: UUID
) -> Optional[List[Union[PostDto, QuotePostDto, RepostDto]]]:
    if only_follower:
        posts = post_repo.get_following_posts(db, params, user_id)

        if not posts:
            return []

        return _post_list_to_dto(posts)

    posts = post_repo.get_posts(db, params)
    if not posts:
        return []

    return _post_list_to_dto(posts)


def create_repost(db: Session, new_repost: CreateRepost) -> RepostDto:
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
        created = post_repo.save_post(db, post)

        return RepostDto(
            id=created.id,
            created_at=created.created_at,
            type=created.type,
            user=UserDto(
                id=created.user.id,
                username=created.user.username,
                joined_date=created.user.joined_date,
            ),
            refered_post=PostDto(
                id=created.refered_post.id,
                text=created.refered_post.id,
                created_at=created.refered_post.id,
                type=created.refered_post.id,
                user=UserDto(
                    id=created.refered_post.user.id,
                    username=created.refered_post.user.username,
                    joined_date=created.refered_post.user.joined_date,
                ),
            ),
        )

    return


def create_quote(db: Session, new_quote: CreateQuote) -> QuotePostDto:
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
        created = post_repo.save_post(db, post)

        return QuotePostDto(
            id=created.id,
            text=created.text,
            created_at=created.created_at,
            type=created.type,
            user=UserDto(
                id=created.user.id,
                username=created.user.username,
                joined_date=created.user.joined_date,
            ),
            refered_post=PostDto(
                id=created.refered_post.id,
                text=created.refered_post.id,
                created_at=created.refered_post.id,
                type=created.refered_post.id,
                user=UserDto(
                    id=created.refered_post.user.id,
                    username=created.refered_post.user.username,
                    joined_date=created.refered_post.user.joined_date,
                ),
            ),
        )

    return


def create_post(db: Session, new_post: CreatePost) -> PostDto:
    if user_service.get_user(db, new_post.author_id) and _can_user_post(
        db, new_post.author_id
    ):
        post = Post(text=new_post.text, author_id=new_post.author_id)
        created = post_repo.save_post(db, post)

        return PostDto(
            id=created.id,
            text=created.text,
            created_at=created.created_at,
            type=created.type,
            user=UserDto(
                id=created.user.id,
                username=created.user.username,
                joined_date=created.user.joined_date,
            ),
        )

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
) -> List[Union[PostDto, QuotePostDto, RepostDto]]:
    posts = post_repo.get_posts_by_author(db, params, author_id)
    return _post_list_to_dto(posts)


def _post_list_to_dto(posts: Any) -> List[Union[QuotePostDto, RepostDto, PostDto]]:
    result = []
    for post in posts:
        if post.type == PostTypes.DEFAULT:
            result.append(
                PostDto(
                    id=post.id,
                    text=post.text,
                    created_at=post.created_at,
                    type=post.type,
                    user=UserDto(id=post.user.id, username=post.user.username),
                )
            )

        if post.type == PostTypes.REPOST:
            result.append(
                RepostDto(
                    id=post.id,
                    created_at=post.created_at,
                    type=post.type,
                    user=UserDto(
                        id=post.user.id,
                        username=post.user.username,
                        joined_date=post.user.joined_date,
                    ),
                    refered_post=PostDto(
                        id=post.refered_post.id,
                        text=post.refered_post.id,
                        created_at=post.refered_post.id,
                        type=post.refered_post.id,
                        user=UserDto(
                            id=post.refered_post.user.id,
                            username=post.refered_post.user.username,
                            joined_date=post.refered_post.user.joined_date,
                        ),
                    ),
                )
            )

        if post.type == PostTypes.QUOTED:
            result.append(
                QuotePostDto(
                    id=post.id,
                    text=post.text,
                    created_at=post.created_at,
                    type=post.type,
                    user=UserDto(
                        id=post.user.id,
                        username=post.user.username,
                        joined_date=post.user.joined_date,
                    ),
                    refered_post=PostDto(
                        id=post.refered_post.id,
                        text=post.refered_post.id,
                        created_at=post.refered_post.id,
                        type=post.refered_post.id,
                        user=UserDto(
                            id=post.refered_post.user.id,
                            username=post.refered_post.user.username,
                            joined_date=post.refered_post.user.joined_date,
                        ),
                    ),
                )
            )

    return result
