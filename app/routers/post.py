from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.Post])
def get_posts_list(
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    #cursor.execute(
    #    """SELECT * FROM posts;"""
    #)
    #posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.CreatePost, 
    db: Session = Depends(get_db),
    # Constraint/Dependency to check Is User Authenticatated, Access to it if only True and user provide JWT token in body request
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
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
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retrieve created post (RETURNING *)
    
    return new_post


@router.get('/latest', response_model=schemas.Post)
def get_latest_post(
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    #cursor.execute(
    #    """
    #    SELECT * FROM posts 
    #    ORDER BY created_at DESC
    #    LIMIT 1;
    #    """
    #)
    #latest_post = cursor.fetchone()
    latest_post = db.query(models.Post).order_by(
        models.Post.created_at.desc()).first()
    
    return latest_post


@router.get('/{id}', response_model=schemas.Post)
def get_post_detail(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id=} was not found")

    return post


@router.put('/{id}', response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.UpdatePost, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
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
    
    post_query = db.query(models.Post).filter_by(id=id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id=} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"not authorized to perform this action")
    
    #post_query.update({'title': 'this is updated post title', 'content': 'some updated content'}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
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
    
    post_query = db.query(models.Post).filter_by(id=id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id=} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"not authorized to perform this action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
