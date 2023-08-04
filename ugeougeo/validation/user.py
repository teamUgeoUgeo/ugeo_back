from pydantic import BaseModel, validator, EmailStr


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


class PatchUserInfo(BaseModel):
    username: str = None
    nickname: str = None
    email: str = None


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
