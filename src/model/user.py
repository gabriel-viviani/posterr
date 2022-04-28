from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from datetime import date
from uuid import uuid4

from src.repository.database import Base
from src.config import generate_today


class Follow(Base):
    __tablename__ = "follow"

    follower_id = Column(ForeignKey("user.id"), UUID(as_uuid=True), primary_key=True)
    following_id = Column(ForeignKey("user.id"), UUID(as_uuid=True), primary_key=True)
    since = Column(Date, default=generate_today())

    def __init__(self, follower_id: UUID, following_id: UUID, since: date) -> None:
        self.follower_id = follower_id
        self.following_id = following_id
        self.since = since


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, primary_key=True, length=14)
    joined_date = Column(Date, default=generate_today())

    followers = relationship(
        "User",
        secondary=Follow,
        primaryjoin=id == Follow.following_id,
        secondaryjoin=id == Follow.follower_id,
        backref=backref("children"),
    )

    posts = relationship("Post", back_populates="user")

    def __init__(self, username: str) -> None:
        self.username = username
