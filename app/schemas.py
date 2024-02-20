from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


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
