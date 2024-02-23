from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# Users
class UserBase(BaseModel):
    email: EmailStr
    password: str


class CreateUser(UserBase):
    pass


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    

# Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserInfo

    # convert sqlalchemy model to dict that pydantic will handle
    class Config:
        from_attributes = True  # Renamed from orm_mode


# Auth
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # TODO: remove Optional typing
    id: Optional[str] = None


# Votes

class Vote(BaseModel):
    post_id: int
    direction: bool
