from datetime import timedelta, datetime

from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from pydantic import EmailStr

from database import get_db
from user import Validation, create, get_existing_user, get_user, pwd_context, Token
from config import const

router = APIRouter(
    prefix="/api/user",
)


@router.post("/login", response_model=Token, tags=['AUTH'], summary="로그인")
def login_for_access_token(email: str,
                           password: str,
                           db: Session = Depends(get_db)):

    form_data: OAuth2PasswordRequestForm = OAuth2PasswordRequestForm(
        username=email,
        password=password,
        grant_type="",
        scope="",
        client_id="",
        client_secret="")

    user = get_user(db, EmailStr(form_data.username))
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, const.SECRET_KEY, algorithm=const.ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email
    }


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, tags=['AUTH'], summary="회원가입")
def user_create(_user_create: Validation, db: Session = Depends(get_db)):
    user = get_existing_user(db, validation=_user_create)
    if user:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    create(db=db, validation=_user_create)