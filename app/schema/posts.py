from pydantic import BaseModel
from datetime import datetime
from app.schema import users


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class GetPost(PostBase):
    id: int
    created_time: datetime
    owner_id: int
    owner: users.UserBase

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    pass
