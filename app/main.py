from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(vote.router)
app.include_router(user.router)
app.include_router(auth.router)

app.get('/', tags=["Welcome Home Page"])(lambda: {
    "message": "Welcome to my Social Media API powered by FastAPI, API documentation in '/docs' endpoint.",
    "source_code": "https://github.com/dotpep/social-media-api"})
