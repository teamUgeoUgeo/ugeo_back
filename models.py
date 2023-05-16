from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    nickname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    create_at = Column(DateTime, nullable=False)
    detail = Column(Text, unique=True, nullable=False)
    user = relationship("User", backref="article_users")
