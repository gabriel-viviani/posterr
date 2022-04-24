from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class UserDto(BaseModel):
    id: UUID
    username: str
    joined_date: datetime
    followers: int
    following: int
