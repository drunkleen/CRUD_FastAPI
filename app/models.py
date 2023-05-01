from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.expression import text
from .database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String, index=True, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    mail = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_time = Column(DateTime(timezone=True), nullable=False, default=func.now())


class Favorite(Base):
    __tablename__ = 'favorites'

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)


class IPLog(Base):
    __tablename__ = 'iplog'

    id = Column(Integer, primary_key=True, nullable=False)
    user_mail = Column(String, index=True, nullable=False)
    user_browser = Column(String, index=True, nullable=False)
    user_os = Column(String, index=True, nullable=False)
    user_device = Column(String, index=True, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
