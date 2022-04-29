from fastapi_pagination import Params, Page as BasePage
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Union, List

from src.dto.post import (
    PostDto,
    CreatePost,
    CreateQuote,
    CreateRepost,
    QuotePostDto,
    RepostDto,
)
from src.service import post as post_service
from src.repository.database import get_db

Page = BasePage.with_custom_options(size=10)
router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Page[List[Union[PostDto, QuotePostDto, RepostDto]]],
)
def get_all(
    params: Params,
    db: Session = Depends(get_db),
    only_follower: bool = False,
    user_id: str = None,
) -> Page[List[Union[PostDto, QuotePostDto, RepostDto]]]:
    return post_service.get_posts(db, params, only_follower, user_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDto)
def create_post(new_post: CreatePost, db: Session = Depends(get_db)) -> PostDto:
    return post_service.create_post(db, new_post)


@router.post("/repost", status_code=status.HTTP_201_CREATED, response_model=PostDto)
def create_repost(new_repost: CreateRepost, db: Session = Depends(get_db)) -> PostDto:
    return post_service.create_repost(db, new_repost)


@router.post("/quote", status_code=status.HTTP_201_CREATED, response_model=PostDto)
def create_quote(new_quote: CreateQuote, db: Session = Depends(get_db)) -> PostDto:
    return post_service.create_quote(db, new_quote)
