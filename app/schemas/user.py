from pydantic import BaseModel, EmailStr
from datetime import datetime


class IUserBase(BaseModel):
    email: EmailStr
    password: str


class ICreateUser(IUserBase):
    pass


class IUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True


class IUserInfo(BaseModel):
    id: int
    email: EmailStr
