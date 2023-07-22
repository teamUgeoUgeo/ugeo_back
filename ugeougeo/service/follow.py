from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator

from ugeougeo.models import Follow, User
from ugeougeo.service import user as user_service
from ugeougeo.validation import user as user_validation


class Validation(BaseModel):
    id: int
    follow_user: user_validation.Validation
    be_followed_user: user_validation.Validation


class FollowCreate(BaseModel):
    be_followed_user: int

    @validator('be_followed_user')
    def check_be_followed_user_empty(cls, v):
        if not v:
            raise ValueError('팔로우 할 대상이 없습니다.')
        return v




def create_follow(db: Session, follow_create: FollowCreate,
                  follow_user_validation: User):
    
    be_followed_user_validation = user_service.get_user_by_id(db, id=follow_create.be_followed_user)
    
    db_comment = Follow(follow_user=follow_user_validation,
                         be_followed_user=be_followed_user_validation)

    
    db.add(db_comment)
    db.commit()
    db.flush()

    return db_comment