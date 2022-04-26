from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.dto.user import UserDto
from src.repository import user as user_repo


def get_user(db: Session, user_id: UUID) -> UserDto:
    if _user_exists:
        user = user_repo.get_user_by_id(db, user_id)

        return UserDto(
            id=user.id,
            username=user.username,
            joined_date=user.joined_date,
            followers=len(user.followers),
            following=user_repo.get_user_following_num(db, user_id),
        )


def _user_exists(db: Session, user_id: UUID) -> bool:
    author = user_repo.get_user_by_id(db, user_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_id} does not exist.",
        )

    return True
