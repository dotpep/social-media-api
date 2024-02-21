from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users/posts",
    tags=['Users', 'Posts']
)


@router.get('/', response_model=List[schemas.Post])
def get_user_posts_list(
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).filter_by(owner_id=current_user.id).all()
    return posts


@router.get('/{id}', response_model=schemas.Post)
def get_user_post_detail(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter_by(id=id, owner_id=current_user.id).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id=} was not found")

    return post