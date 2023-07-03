from pydantic import BaseModel, validator, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
from models import User


class Validation(BaseModel):
    username: str
    nickname: str
    email: EmailStr
    password: str

    @validator('username', 'password', 'email', 'nickname')
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return value


class EmailValid(BaseModel):
    email: EmailStr

    @validator('email')
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return value


class UsernameValid(BaseModel):
    username: str

    @validator('username')
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return value


class Token(BaseModel):
    access_token: str
    token_type: str
    email: EmailStr
    username: str
    nickname: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create(db: Session, validation: Validation):
    db_user = User(username=validation.username,
                   nickname=validation.nickname,
                   password=pwd_context.hash(validation.password),
                   email=validation.email)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, validation: Validation):
    return db.query(User).filter((User.username == validation.username)
                                 | (User.email == validation.email)).first()


def get_user(db: Session, email: EmailStr) -> models.User | None:
    return db.query(User).filter(User.email == email).first()


def get_exist_email(db: Session, _email: EmailValid):
    return db.query(User).filter(User.email == _email.email).first()


def get_exist_username(db: Session, _username: UsernameValid):
    return db.query(User).filter(User.username == _username.username).first()
