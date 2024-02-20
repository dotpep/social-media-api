from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    # convert sqlalchemy model to dict that pydantic will handle
    class Config:
        from_attributes = True  # Renamed from orm_mode


# Users
class UserBase(BaseModel):
    email: EmailStr
    password: str


class CreateUser(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True


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
