from fastapi import status, APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ugeougeo.database import get_db
from ugeougeo.models import User
from ugeougeo.router.user import get_current_user
from ugeougeo.service import follow

router = APIRouter(prefix="/api/follow", )

@router.get("/", tags=['Follow'], summary="라우터 테스트")
def test_follow_router():
    return "테스트"

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             summary="일방적 팔로우",
             tags=['Follow'])
def post_follow(_follow_create: follow.FollowCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    
    
    db_follow: follow = follow.create_follow(
        db=db,
        follow_create=_follow_create,
        follow_user_validation=current_user
    )
    return {'be_followed_user': db_follow.be_followed_user}