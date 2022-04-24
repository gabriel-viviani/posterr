from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src.repository.database import Base
from src.config import generate_now
from src.dto.post import PostTypes


class Post(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String, length=777, nullable=True)
    created_at = Column(DateTime, default=generate_now())
    author_id = Column(ForeignKey("user.id"), UUID(as_uuid=True))
    type = Column(Enum(PostTypes), nullable=False, default=PostTypes.DEFAULT)

    refered_post_id = Column(ForeignKey("post.id"), UUID(as_uuid=True), nullable=True)

    user = relationship("User", back_populates="posts")
    refered_post = relationship("Post", backref=backref("parent", remote_side=[id]))

    def __init__(self, 
