import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator

from models import Comment, Article, User
from service import article
import user

class Validation(BaseModel):
    id: int
    create_at: datetime.datetime
    detail: str
    user: user.Validation
    article: article.Validation

class CommentCreate(BaseModel):
    detail: str
    article_id: int
    
    @validator('detail')
    def check_detail_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('댓글 내용이 없습니다.')
        return v
    
    @validator('article_id')
    def check_article_id_empty(cls, v):
        if not v:
            raise ValueError('게시글이 없습니다.')
        return v

def create_comment(db: Session, comment_create: CommentCreate,
                   user_validation: User, article_validation: Article):
    
    db_comment = Comment(detail=comment_create.detail,
                         create_at=datetime.datetime.now(),
                         user=user_validation,
                         article=article_validation)

    db.add(db_comment)
    db.commit()
    db.flush()

    return db_comment.id