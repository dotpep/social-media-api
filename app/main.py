from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

app.get('/', tags=["Welcome Home Page"])(lambda: {
    "message": "Welcome to my Social Media API powered by FastAPI, API documentation in '/docs' endpoint"})
