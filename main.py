from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = Field(None, ge=1, le=5)


@app.get('/')
def root():
    return {"message": "Welcome to my API"}


@app.get('/posts')
def get_posts():
    return {"data": "This is your posts"}


@app.post('/create')
def create_post_payload(paylaod: dict = Body(...)):
    return {"new_post": {"title": paylaod["title"], "content": paylaod["content"]}}


@app.post('/posts/create')
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data": "new post"}
