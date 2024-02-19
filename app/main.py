from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

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


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get('/')
def root():
    return {"message": "Welcome to my API"}


@app.get('/posts')
def get_posts_list():
    cursor.execute(
        """SELECT * FROM posts;"""
    )
    posts = cursor.fetchall()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """
        INSERT INTO posts (title, content, published) 
        VALUES (%s, %s, %s) 
        RETURNING *;
        """,
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    
    conn.commit()
    
    print("Post Succesfully Created: ", new_post)
    return {"data": new_post}


@app.get('/posts/latest')
def get_latest_post():
    cursor.execute(
        """
        SELECT * FROM posts 
        ORDER BY created_at DESC
        LIMIT 1;
        """
    )
    latest_post = cursor.fetchone()
    
    return {"detail": latest_post}


@app.get('/posts/{id}')
def get_post_detail(id: int):
    cursor.execute(
        """
        SELECT * FROM posts 
        WHERE id = %s;
        """,
        (str(id), )
    )
    post = cursor.fetchone()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")

    return {"post_details": post}


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *;
        """,
        (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")
    
    print("Post Succesfully Updated: ", updated_post)
    return {"data": updated_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """
        DELETE FROM posts
        WHERE id = %s
        RETURNING *;
        """,
        (str(id), )
    )
    deleted_post = cursor.fetchone()

    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")
    
    print("Post Succesfully Deleted: ", deleted_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
