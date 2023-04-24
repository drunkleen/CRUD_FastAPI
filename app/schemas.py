from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# //////////////////////////////// User Side ////////////////////////////////
class UserBase(BaseModel):
    mail: EmailStr

    class Config:
        orm_mode = True


class GetUser(UserBase):
    id: int
    created_time: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


# //////////////////////////////// Posts ////////////////////////////////
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class GetPost(PostBase):
    id: int
    created_time: datetime
    owner_id: int
    owner: UserBase

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    pass


# ////////////////////////////// Favorite ///////////////////////////////
class FavoriteBase(BaseModel):
    post_id: int
    dir: bool


# //////////////////////////////// AUTH ////////////////////////////////
class UserLogin(BaseModel):
    mail: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    # class Config:
    #     orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

    # token_type: str

    class Config:
        orm_mode = True
