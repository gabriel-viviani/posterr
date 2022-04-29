from sqlalchemy import Column, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src.repository.database import Base
from src.config import generate_today
from src.dto.post import PostTypes


class Post(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String(length=777), nullable=True)
    created_at = Column(Date, default=generate_today())
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    type = Column(Enum(PostTypes), nullable=False, default=PostTypes.DEFAULT)

    refered_post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=True)

    user = relationship("User", back_populates="posts")
    refered_post = relationship("Post", backref=backref("parent", remote_side=[id]))

    def __init__(self, text, author_id, type, refered_post_id=None):
        self.text = text
        self.author_id = author_id
        if type:
            self.type = type
        if refered_post_id:
            self.refered_post_id
