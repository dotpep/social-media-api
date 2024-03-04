from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.v1 import post, vote, user, auth

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
    "message": "Welcome to my Social Media API powered by FastAPI, API documentation in '/docs' and `/redoc` endpoint. Successfully CI/CD pipeline deployment!",
    "source_code": "https://github.com/dotpep/social-media-api",
    "domain_name": "https://dotpep.xyz/"})


@app.get('/root', tags=["Welcome Home Page"], status_code=200)
def root():
    return {"message": "Hello Dear Developer"}
