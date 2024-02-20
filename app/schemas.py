from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
