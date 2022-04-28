from pydantic import BaseModel, constr
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
    type: PostTypes

    user: UserDto


class CreatePost(BaseModel):
    text: constr(max_lenght=777, min_length=1, strip_whitespace=True)
    type: PostTypes = PostTypes.DEFAULT
    author_id: UUID


class CreateQuote(BaseModel):
    referred_post_id: UUID
    quote_text: constr(max_lenght=777, min_length=1, strip_whitespace=True)
    author_id: UUID
    type: PostTypes = PostTypes.QUOTED


class CreateRepost(CreatePost):
    referred_post_id: UUID
    author_id: UUID
    type: PostTypes = PostTypes.REPOST
