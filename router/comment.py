from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Comment, User
from router.user import get_current_user
from user import Validation, get_user
from service import comment, article


router = APIRouter(prefix="/api/comment", )

@router.get("/api_test", tags=['Comment'], summary="라우터 테스트")
def get_article_list():
    return {"key": 'value'}

@router.post("/",
             status_code=status.HTTP_204_NO_CONTENT,
             summary="댓글 작성",
             tags=['Comment'])
def post_comment(_comment_create: comment.CommentCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    
    db_article = article.get_article(db, article_id=_comment_create.article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="게시글이 존재하지 않습니다.")
    
    db_comment = comment.create_comment(db=db,
                                        comment_create=_comment_create,
                                        user_validation=current_user,
                                        article_validation=db_article)
    
