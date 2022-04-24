from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from repository.database import get_db
from src.service.post import get_posts, create_post
from src.dto.post import PostDto, CreatePost, CreateQuote, CreateRepost

router = APIRouter()


@router.get("/", status.HTTP_200_OK)
def get_all(
    db: Session = Depends(get_db),
    limit: int = 10,
    only_follower: bool = False,
    user_id: str = None,
) -> List[PostDto]:
    return get_posts(db, limit, only_follower, user_id)

@router.post("/", status.HTTP_201_CREATED)
def create_post(db: Session = Depends(get_db), new_post: CreatePost) -> None:
    return create_post(db, new_post)
