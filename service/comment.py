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

class CommentRead(BaseModel):
    article_id: int

def create_comment(db: Session, comment_create: CommentCreate,
                   user_validation: User, article_validation: Article):
    
    db_comment = Comment(detail=comment_create.detail,
                         create_at=datetime.datetime.now(),
                         user=user_validation,
                         article=article_validation)

    db.add(db_comment)
    db.commit()
    db.flush()

    return db_comment

def get_comment_list(db: Session, article_id: int, user_id: int):
    responses = db.query(Comment, User.username, User.nickname).order_by(desc(Comment.create_at)
        ).filter(Article.id==Comment.article_id).filter(Comment.article_id==article_id
        ).filter(User.id==Comment.user_id).filter(Comment.user_id==user_id).all()
    output_response = []
    for response in responses:
        converted_response = {
            'id': response[0].id,
            'detail': response[0].detail,
            'create_at': response[0].create_at,
            'username': response[1],
            'nickname': response[2]
        }
        output_response.append(converted_response)
    return output_response

def get_comment(db: Session, comment_id: int):
    comment = db.query(Comment).get(comment_id)
    return comment
