import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator

from models import Article, User
import user


class Validation(BaseModel):
    id: int
    amount: int
    create_at: datetime.datetime
    detail: str
    user: user.Validation | None

    class Config:
        orm_mode = True


class ArticleCreate(BaseModel):
    amount: int
    detail: str

    @validator('detail')
    def check_detail_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('지출 내역이 비어있습니다.')
        return v

    @validator('amount')
    def check_amount_empty(cls, v):
        if not v:
            raise ValueError('금액이 비어있습니다.')
        return v


def create_article(db: Session, article_create: ArticleCreate,
                   user_validation: User):
    db_question = Article(amount=article_create.amount,
        detail=article_create.detail,
        create_at=datetime.datetime.now(),
        user=user_validation)
    db.add(db_question)
    db.commit()

