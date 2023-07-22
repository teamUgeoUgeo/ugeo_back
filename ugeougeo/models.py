from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ugeougeo.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    nickname = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    create_at = Column(DateTime, nullable=False)
    detail = Column(String(255), nullable=False)
    user = relationship("User", backref="article_users")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    create_at = Column(DateTime)
    detail = Column(String(140))
    user = relationship("User")
    article = relationship("Article")


class Follow(Base):
    __tablename__ = "follow"

    id = Column(Integer, primary_key=True)
    follow_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    be_followed_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    follow = relationship("User", foreign_keys=[follow_user])
    be_followed = relationship("User", foreign_keys=[be_followed_user])
