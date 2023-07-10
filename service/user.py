from pydantic import EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from validation import user
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create(db: Session, validation: user.Validation):
    db_user = User(username=validation.username,
                   nickname=validation.nickname,
                   password=pwd_context.hash(validation.password),
                   email=validation.email)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, validation: user.Validation):
    return db.query(User).filter((User.username == validation.username)
                                 | (User.email == validation.email)).first()


def get_user_by_email(db: Session, email: EmailStr) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, id: int) -> User | None:
    return db.query(User).filter(User.id == id).first()


def get_exist_email(db: Session, _email: user.EmailValid):
    return db.query(User).filter(User.email == _email.email).first()


def get_exist_username(db: Session, _username: user.UsernameValid):
    return db.query(User).filter(User.username == _username.username).first()


def update(db: Session, db_user: User, user_update: user.Validation):
    db_user.email = user_update.email
    db_user.username = user_update.username
    db_user.nickname = user_update.nickname
    db_user.password = pwd_context.hash(user_update.password)
    db.add(db_user)
    db.commit()
