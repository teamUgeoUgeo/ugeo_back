from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ugeougeo.database import get_db
from ugeougeo.models import Article, User
from ugeougeo.router.user import get_current_user
from ugeougeo.service import article

router = APIRouter(prefix="/api/article", )


@router.get("/", tags=['Article'], summary="게시글 목록 조회")
def get_article_list(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return article.get_article_list(db, user_id=current_user.id)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             summary="게시글 작성",
             tags=['Article'])
def post_article(_article_create: article.ArticleCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    db_article = article.create_article(db=db,
                                        article_create=_article_create,
                                        user_validation=current_user)

    return {'article_id': db_article.id, 'created_at': db_article.create_at}


@router.put("/",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="게시글 수정",
            tags=['Article'])
def edit_article(_article_update: article.ArticleUpdate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    db_article = article.get_article(db, article_id=_article_update.article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_article.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    article.update_question(db=db,
                            db_article=db_article,
                            article_update=_article_update)


@router.delete("/{article_id:int}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="게시글 삭제",
               tags=['Article'])
def delete_article(article_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_article = article.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_article.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    article.delete_question(db=db, db_article=db_article)
