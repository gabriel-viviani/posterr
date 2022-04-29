from pydantic import BaseModel, constr
from datetime import date
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
    created_at: date
    type: PostTypes

    user: UserDto


class QuotePostDto(PostDto):
    refered_post: PostDto


class RepostDto(BaseModel):
    id: UUID
    created_at: date
    type: PostTypes

    user: UserDto
    refered_post: PostDto


class CreatePost(BaseModel):
    text: constr(max_length=777, min_length=1, strip_whitespace=True)
    type: PostTypes = PostTypes.DEFAULT
    author_id: UUID


class CreateQuote(BaseModel):
    referred_post_id: UUID
    quote_text: constr(max_length=777, min_length=1, strip_whitespace=True)
    author_id: UUID
    type: PostTypes = PostTypes.QUOTED


class CreateRepost(BaseModel):
    referred_post_id: UUID
    author_id: UUID
    type: PostTypes = PostTypes.REPOST
