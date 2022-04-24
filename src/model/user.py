from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src.repository.database import Base
from src.config import generate_now


class Follow(Base):
    __tablename__ = "follow"

    follower_id = Column(ForeignKey("user.id"), UUID(as_uuid=True), primary_key=True)
    followed_id = Column(ForeignKey("user.id"), UUID(as_uuid=True), primary_key=True)
    since = Column(DateTime, default=generate_now())


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, primary_key=True, length=14)
    joined_date = Column(DateTime, default=generate_now())

    followers = relationship(
        "User",
        secondary=Follow,
        primaryjoin=id == Follow.follower_id,
        secondaryjoin=id == Follow.followed_id,
        backref=backref("children"),
    )

    posts = relationship("Post", back_populates="user")
