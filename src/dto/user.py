from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID


class UserDto(BaseModel):
    id: UUID
    username: str
    joined_date: date
    followers: Optional[int]
    following: Optional[int]


class UserFollow(BaseModel):
    followed_id: UUID
