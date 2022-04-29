from sqlalchemy import Column, Date, ForeignKey, String, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from datetime import date
from uuid import uuid4

from src.repository.database import Base
from src.config import generate_today

following = Table(
    "follow",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("follower_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("following_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    username = Column(String(length=14), primary_key=True)
    joined_date = Column(Date, default=generate_today())

    following = relationship(
        "User",
        secondary=following,
        primaryjoin=id == following.c.follower_id,
        secondaryjoin=id == following.c.following_id,
        backref=backref("children"),
    )

    posts = relationship("Post", back_populates="user")

    def __init__(self, username: str) -> None:
        self.username = username
