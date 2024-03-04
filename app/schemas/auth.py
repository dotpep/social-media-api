from pydantic import BaseModel, EmailStr
from typing import Optional


class IUserLogin(BaseModel):
    email: EmailStr
    password: str


class IToken(BaseModel):
    access_token: str
    token_type: str


class ITokenData(BaseModel):
    # TODO: remove Optional typing
    id: Optional[str] = None