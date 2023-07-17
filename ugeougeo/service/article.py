import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator

from ugeougeo.models import Article, User
from ugeougeo.validation import user


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


class ArticleUpdate(ArticleCreate):
    article_id: int


def create_article(db: Session, article_create: ArticleCreate,
                   user_validation: User):
    db_article = Article(amount=article_create.amount,
                         detail=article_create.detail,
                         create_at=datetime.datetime.now(),
                         user=user_validation)
    db.add(db_article)
    db.commit()
    db.flush()

    return db_article


def get_article_list(db: Session, user_id: int):
    responses = db.query(Article, User.username, User.nickname).order_by(
        desc(Article.create_at)).filter(User.id == Article.user_id).filter(
            Article.user_id == user_id).all()

    output_response = []
    for response in responses:
        converted_response = {
            'id': response[0].id,
            'detail': response[0].detail,
            'amount': response[0].amount,
            'create_at': response[0].create_at,
            'username': response[1],
            'nickname': response[2]
        }
        output_response.append(converted_response)
    return output_response


def get_article(db: Session, article_id: int):
    article = db.query(Article).get(article_id)
    return article


def delete_question(db: Session, db_article: Article):
    db.delete(db_article)
    db.commit()


def update_question(db: Session, db_article: Article,
                    article_update: ArticleUpdate):
    db_article.detail = article_update.detail
    db_article.amount = article_update.amount
    db.add(db_article)
    db.commit()
