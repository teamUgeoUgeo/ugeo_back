from fastapi import status, APIRouter, Depends, HTTPException, Response, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Comment, User
from router.user import get_current_user
from user import Validation, get_user
from service import comment, article

router = APIRouter(prefix="/api/comment", )


@router.get("/{article_id:int}", tags=['Comment'], summary="댓글 목록 조회")
def get_comment_list(article_id: int,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return comment.get_comment_list(db,
                                    article_id=article_id,
                                    user_id=current_user.id)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             summary="댓글 작성",
             tags=['Comment'])
def post_comment(_comment_create: comment.CommentCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):

    db_article = article.get_article(db, article_id=_comment_create.article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="게시글이 존재하지 않습니다.")

    db_comment: comment = comment.create_comment(
        db=db,
        comment_create=_comment_create,
        user_validation=current_user,
        article_validation=db_article)

    return {'created_at': db_comment.create_at, 'comment_id': db_comment.id}


@router.put("/{comment_id: int}",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="댓글 수정",
            tags=['Comment'])
def edit_comment(comment_id: int,
                 comment_detail=Query(),
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    db_comment = comment.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_comment.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    comment.update_comment(db=db,
                           db_comment=db_comment,
                           comment_datail=comment_detail)


@router.delete("/{comment_id:int}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="댓글 삭제",
               tags=['Comment'])
def delete_comment(comment_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_comment = comment.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_comment.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    comment.delete_comment(db=db, db_comment=db_comment)
