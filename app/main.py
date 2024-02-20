from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Connect postgres DB
while True:
    try:
        conn = psycopg2.connect(
            dbname="social_media_fastapi",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was established successfully!")
        break
    except Exception as error:
        print("Failed to connect database!")
        print("Exception Error: ", error)
        time.sleep(10)


@app.get('/')
def root():
    return {"message": "Welcome to my API"}


@app.get('/posts')
def get_posts_list(db: Session = Depends(get_db)):
    #cursor.execute(
    #    """SELECT * FROM posts;"""
    #)
    #posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreateUpdatePost, db: Session = Depends(get_db)):
    #cursor.execute(
    #    """
    #    INSERT INTO posts (title, content, published) 
    #    VALUES (%s, %s, %s) 
    #    RETURNING *;
    #    """,
    #    (post.title, post.content, post.published)
    #)
    #new_post = cursor.fetchone()
    #conn.commit()
    
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retrieve created post (RETURNING *)
    
    return {"data": new_post}


@app.get('/posts/latest')
def get_latest_post(db: Session = Depends(get_db)):
    #cursor.execute(
    #    """
    #    SELECT * FROM posts 
    #    ORDER BY created_at DESC
    #    LIMIT 1;
    #    """
    #)
    #latest_post = cursor.fetchone()
    # TODO: add pydantic Post schemas created_at property and assign it instead of id.desc() 
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    
    return {"detail": latest_post}


@app.get('/posts/{id}')
def get_post_detail(id: int, db: Session = Depends(get_db)):
    #cursor.execute(
    #    """
    #    SELECT * FROM posts 
    #    WHERE id = %s;
    #    """,
    #    (str(id), )
    #)
    #post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post).filter_by(id=id).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")

    return {"post_details": post}


@app.put('/posts/{id}')
def update_post(id: int, updated_post: schemas.CreateUpdatePost, db: Session = Depends(get_db)):
    #cursor.execute(
    #    """
    #    UPDATE posts
    #    SET title = %s, content = %s, published = %s
    #    WHERE id = %s
    #    RETURNING *;
    #    """,
    #    (post.title, post.content, post.published, str(id))
    #)
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    post = db.query(models.Post).filter_by(id=id)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")
    
    #post_query.update({'title': 'this is updated post title', 'content': 'some updated content'}, synchronize_session=False)
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return {"data": post.first()}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute(
    #    """
    #    DELETE FROM posts
    #    WHERE id = %s
    #    RETURNING *;
    #    """,
    #    (str(id), )
    #)
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    post = db.query(models.Post).filter_by(id=id)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
