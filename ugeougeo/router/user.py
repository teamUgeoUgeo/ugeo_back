from datetime import timedelta, datetime

from fastapi import APIRouter, Body, Header
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ugeougeo.database import get_db
from ugeougeo.validation import user as user_validation
from ugeougeo.service import user as user_service
from ugeougeo.config import const
from ugeougeo.models import User
from ugeougeo.service import article

router = APIRouter(prefix="/api/user", )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/test_login")


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
        user = user_service.get_user_by_email(db, email=EmailStr(email))
        if user is None:
            raise credentials_exception
        return user


@router.post("/test_login",
             response_model=user_validation.Token,
             tags=['AUTH'],
             summary="로그인")
def login_for_test(form_data: OAuth2PasswordRequestForm = Depends(),
                   db: Session = Depends(get_db)):

    return _create_token(db, form_data)


@router.post("/login",
             response_model=user_validation.Token,
             tags=['AUTH'],
             summary="로그인")
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


@router.post("/create",
             status_code=status.HTTP_204_NO_CONTENT,
             tags=['AUTH'],
             summary="회원가입")
def user_create(_user_create: user_validation.Validation,
                db: Session = Depends(get_db)):
    user = user_service.get_existing_user(db, validation=_user_create)
    if user:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_service.create(db=db, validation=_user_create)


@router.post("/check_email",
             status_code=status.HTTP_200_OK,
             tags=['AUTH'],
             summary="이메일 중복확인")
def check_email(_email: user_validation.EmailValid,
                db: Session = Depends(get_db)):
    is_exist = user_service.get_exist_email(db, _email=_email)
    if is_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="사용 중인 이메일 입니다")

    return


@router.patch("/info",
              status_code=status.HTTP_204_NO_CONTENT,
              summary="유저 정보 수정",
              tags=['AUTH'])
def edit_user_info(_user_update: user_validation.PatchUserInfo,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_user = user_service.get_user_by_id(db, id=current_user.id)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")

    update_data = _user_update.dict(exclude_unset=True)

    user_service.update_info(update_user=update_data, db=db, db_user=db_user)

    return


@router.patch("/password",
              status_code=status.HTTP_204_NO_CONTENT,
              summary="유저 정보 수정",
              tags=['AUTH'])
def edit_user_password(_user_update: user_validation.PatchPassword,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_user = user_service.get_user_by_id(db, id=current_user.id)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")

    user_service.update_password(update_user=_user_update,
                                 db=db,
                                 db_user=db_user)

    return


@router.post("/check_username",
             status_code=status.HTTP_200_OK,
             tags=['AUTH'],
             summary="유저네임 중복확인")
def check_username(_username: user_validation.UsernameValid,
                   db: Session = Depends(get_db)):
    is_exist = user_service.get_exist_username(db, _username=_username)
    if is_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="사용 중인 이메일 입니다")

    return


@router.get("/search/{username}", tags=['USER'], summary="유저 조회")
def search_user(username: str, db: Session = Depends(get_db)):
    return user_service.search_by_username(db, username)


@router.get("/profile/{username}", tags=['USER'], summary="유저 프로필 조회")
def get_user_profile(username: str,
                     db: Session = Depends(get_db),
                     Authorization: str | None = Header(default=None)):
    db_result = user_service.get_user_by_username(db, username)
    response = {'username': db_result.username, 'nickname': db_result.nickname}

    if Authorization is not None:
        response['articles'] = article.get_article_list(db, db_result.id)

    return response


def _create_token(db: Session, form_data: OAuth2PasswordRequestForm):
    user = user_service.get_user_by_email(db, EmailStr(form_data.username))
    if not user or not user_service.pwd_context.verify(form_data.password,
                                                       user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "sub":
        user.email,
        "exp":
        datetime.utcnow() +
        timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data,
                              const.SECRET_KEY,
                              algorithm=const.ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email,
        "nickname": user.nickname,
        "username": user.username
    }
