from fastapi_pagination import Params, Page as BasePage
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Union
from uuid import UUID

from src.dto.post import PostDto, RepostDto, QuotePostDto
from src.service import user as user_service
from src.repository.database import get_db
from src.dto.user import UserDto, UserFollow

Page = BasePage.with_custom_options(size=5)
router = APIRouter()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserDto)
def get_user(user_id: UUID, db: Session = Depends(get_db)) -> UserDto:
    return user_service.get_user(db, user_id)


@router.get(
    "/{user_id}/posts",
    status_code=status.HTTP_200_OK,
    response_model=Page[List[Union[PostDto, QuotePostDto, RepostDto]]],
)
def get_user_posts(
    user_id: UUID, params: Params, db: Session = Depends(get_db)
) -> Page[List[Union[PostDto, RepostDto, QuotePostDto]]]:
    return user_service.get_user_posts(db, user_id, params)


@router.post("/{user_id}/follow", status_code=status.HTTP_201_CREATED)
def follow(user_id: UUID, following: UserFollow, db: Session = Depends(get_db)) -> None:
    return user_service.follow_user(db, user_id, following)


@router.delete("/{user_id}/unfollow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(
    user_id: UUID, following: UserFollow, db: Session = Depends(get_db)
) -> None:
    return user_service.unfollow(db, user_id, following)
