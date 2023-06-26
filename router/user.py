from datetime import timedelta, datetime

from fastapi import APIRouter, Body
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import EmailStr

from database import get_db
from user import Validation, create, get_existing_user, get_user, pwd_context, Token, EmailValid, get_exist_email, get_exist_username, UsernameValid
from config import const

router = APIRouter(
    prefix="/api/user",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/test_login")


@router.post("/test_login", response_model=Token, tags=['AUTH'], summary="로그인")
def login_for_test(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    return _create_token(db, form_data)


@router.post("/login", response_model=Token, tags=['AUTH'], summary="로그인")
def login_for_access_token(email: str = Body(description='user email',
                                             example='user@example.com'),
                           password: str = Body(description='user password',
                                                example='sample_password'),
                           db: Session = Depends(get_db)):

    form_data: OAuth2PasswordRequestForm = OAuth2PasswordRequestForm(
        username=email,
        password=password,
        grant_type="",
        scope="",
        client_id="",
        client_secret="")

    return _create_token(db, form_data)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, tags=['AUTH'], summary="회원가입")
def user_create(_user_create: Validation, db: Session = Depends(get_db)):
    user = get_existing_user(db, validation=_user_create)
    if user:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    create(db=db, validation=_user_create)


@router.post("/check_email",
             status_code=status.HTTP_200_OK,
             tags=['AUTH'],
             summary="이메일 중복확인")
def check_email(_email: EmailValid, db: Session = Depends(get_db)):
    is_exist = get_exist_email(db, _email=_email)
    if is_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="사용 중인 이메일 입니다")

    return


@router.post("/check_username",
             status_code=status.HTTP_200_OK,
             tags=['AUTH'],
             summary="유저네임 중복확인")
def check_username(_username: UsernameValid, db: Session = Depends(get_db)):
    is_exist = get_exist_username(db, _username=_username)
    if is_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="사용 중인 이메일 입니다")

    return


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             const.SECRET_KEY,
                             algorithms=[const.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = get_user(db, email=EmailStr(email))
        if user is None:
            raise credentials_exception
        return user


def _create_token(db: Session, form_data: OAuth2PasswordRequestForm):
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
        "email": user.email,
        "nickname": user.nickname,
        "username": user.username
    }