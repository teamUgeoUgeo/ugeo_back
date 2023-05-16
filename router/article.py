from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from models import Article, User
from router.user import get_current_user
from service import article

router = APIRouter(prefix="/api/article", )


@router.get("/", tags=['Article'], summary="게시글 목록 조회")
def get_article_list(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return article.get_article_list(db, user_id=current_user.id)


@router.post("/",
             status_code=status.HTTP_204_NO_CONTENT,
             summary="게시글 작성",
             tags=['Article'])
def post_article(_article_create: article.ArticleCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    article.create_article(db=db,
                           article_create=_article_create,
                           user_validation=current_user)


@router.patch("/{article_id}", summary="게시글 수정", tags=['Article'])
def edit_article():
    pass


@router.delete("/{article_id}", summary="게시글 삭제", tags=['Article'])
def delete_article():
    pass
