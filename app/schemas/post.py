from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from .user import IUserInfo


class IPostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class ICreatePost(IPostBase):
    pass


class IUpdatePost(IPostBase):
    pass


class IPost(IPostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: IUserInfo

    # convert sqlalchemy model to dict that pydantic will handle
    class Config:
        from_attributes = True  # Renamed from orm_mode


class IPostVote(BaseModel):
    Post: IPost
    votes: int

    class Config:
        from_attributes = True
