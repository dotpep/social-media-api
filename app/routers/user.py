from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    email = user.email
    user_query = db.query(models.User).filter_by(email=email).first()
    
    if user.email == user_query.email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"user with {email=} already exists")
    
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get('/{id}', response_model=schemas.User)
def get_specific_user(
    id: int, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter_by(id=id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with {id=} does not exists")

    return user
