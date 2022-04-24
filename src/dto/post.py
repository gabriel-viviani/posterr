from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from enum import Enum

from src.dto.user import UserDto


class PostTypes(str, Enum):
    DEFAULT = "default"
    REPOST = "repost"
    QUOTED = "quoted"


class PostDto(BaseModel):
    id: UUID
    text: str
    created_at: datetime

    user: UserDto


class CreatePost(BaseModel):
    text: str
    type: PostTypes = PostTypes.DEFAULT
    author_id: UUID


class CreateQuote(BaseModel):
    referred_post_id: UUID
    quote_text: str
    author_id: UUID
    type: PostTypes = PostTypes.QUOTED


class CreateRepost(CreatePost):
    referred_post_id: UUID
    author_id: UUID
    type: PostTypes = PostTypes.REPOST
