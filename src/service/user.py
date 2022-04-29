from fastapi import HTTPException, status
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from typing import List, Union
from uuid import UUID

from src.dto.post import PostDto, QuotePostDto, RepostDto
from src.repository import user as user_repo
from src.service import post as post_service
from src.dto.user import UserDto, UserFollow


def get_user(db: Session, user_id: UUID) -> UserDto:
    if _user_exists(db, user_id):
        user = user_repo.get_user_by_id(db, user_id)

        return UserDto(
            id=user.id,
            username=user.username,
            joined_date=user.joined_date,
            followers=len(user.following),
            following=len(user.following),
        )


def _user_exists(db: Session, user_id: UUID) -> bool:
    author = user_repo.get_user_by_id(db, user_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_id} does not exist.",
        )

    return True


def get_user_posts(
    db: Session, params: Params, user_id: UUID
) -> List[Union[PostDto, QuotePostDto, RepostDto]]:
    if _user_exists(db, user_id):
        return post_service.get_posts_by_author_id(db, params, user_id)


def follow_user(db: Session, user_id: UUID, following: UserFollow) -> None:
    if user_id == following.followed_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"A user cannot follow himself.",
        )

    if _user_exists(db, user_id) and _user_exists(db, following.followed_id):
        if _user_already_following(db, user_id, following.followed_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"This user already follows {following.followed_id}",
            )

        user_repo.save_user_follow(db, user_id, following.followed_id)

        return


def _user_already_following(db: Session, follower_id: UUID, followed_id: UUID) -> bool:
    follow = user_repo.get_follow_relation(db, follower_id, followed_id)
    if follow:
        return True


def unfollow(db: Session, follower_id: UUID, follow: UserFollow) -> None:
    followed_id = follow.followed_id

    if follower_id == followed_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="A user cannot unfollow himself.",
        )

    if _user_exists(db, follower_id) and _user_exists(db, followed_id):
        if not _user_already_following(db, follower_id, followed_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {followed_id} is not followed.",
            )

        user_repo.delete_user_follow(db, follower_id, followed_id)
        return
