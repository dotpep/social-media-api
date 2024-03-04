from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from app.models.post import Post
from app.schemas.user import IUser
from app.schemas.vote import Vote
from app.schemas.post import IPost, ICreatePost, IUpdatePost, IPostVote
from app.configs import database
from app.utils import oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get('/', response_model=List[IPostVote])
def get_all_posts(
    db: Session = Depends(database.get_db), 
    current_user: IUser = Depends(oauth2.get_current_user),
    # query params
    limit: int = 5,
    skip: int = 0,
    search: Optional[str] = "",
    owner_id: Optional[int] = None,
    logined_user: Optional[bool] = False
):
    #cursor.execute(
    #    """SELECT * FROM posts;"""
    #)
    #posts = cursor.fetchall()
    
    # TODO: filtering by id and etc query params
    
    #join_vote = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()


    my_post = db.query(Post, func.count(Vote.post_id).label("votes"))
    
    post_join = my_post.join(
        Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id)
    
    post_filter = post_join.filter(Post.title.contains(search))
    if owner_id is not None:
        post_filter = post_filter.filter(Post.owner_id == int(owner_id))
    if logined_user:
        post_filter = post_filter.filter(Post.owner_id == current_user.id)
    
    post_paginate = post_filter.limit(limit).offset(skip)

    return post_paginate.all()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=IPost)
def create_post(
    post: ICreatePost, 
    db: Session = Depends(database.get_db),
    # Constraint/Dependency to check Is User Authenticatated, Access to it if only True and user provide JWT token in body request
    current_user: IUser = Depends(oauth2.get_current_user)
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
    new_post = Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retrieve created post (RETURNING *)
    
    return new_post


@router.get('/latest', response_model=IPostVote)
def get_latest_post(
    db: Session = Depends(database.get_db), 
    current_user: IUser = Depends(oauth2.get_current_user)
):
    #cursor.execute(
    #    """
    #    SELECT * FROM posts 
    #    ORDER BY created_at DESC
    #    LIMIT 1;
    #    """
    #)
    #latest_post = cursor.fetchone()
    
    #join_vote = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    post = db.query(Post, func.count(Vote.post_id).label("votes"))
    
    join_vote = post.join(
        Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id)
    
    latest_post = join_vote.order_by(
        Post.created_at.desc())
    
    return latest_post.first()


@router.get('/{id}', response_model=IPostVote)
def get_specific_post_detail(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: IUser = Depends(oauth2.get_current_user)
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
    
    post = db.query(Post, func.count(Vote.post_id).label("votes"))
    
    join_vote = post.join(
        Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id)
    
    specific_post = join_vote.filter(Post.id == id).first()
    
    if specific_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id=} was not found")

    return specific_post


@router.put('/{id}', response_model=IPost)
def update_post(
    id: int, updated_post: IUpdatePost, 
    db: Session = Depends(database.get_db),
    current_user: IUser = Depends(oauth2.get_current_user)
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
    
    post_query = db.query(Post).filter_by(id=id)
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
    db: Session = Depends(database.get_db),
    current_user: IUser = Depends(oauth2.get_current_user)
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
    
    post_query = db.query(Post).filter_by(id=id)
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
