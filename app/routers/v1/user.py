from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import IUser, ICreateUser
from app.configs import database
from app.utils import auth, oauth2


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=IUser)
def create_user(user: ICreateUser, db: Session = Depends(database.get_db)):
    email = user.email
    existing_user = db.query(User).filter(User.email == email).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"User with email '{email}' already exists")
    
    # hash the password - user.password
    hashed_password = auth.hash(user.password)
    user.password = hashed_password
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get('/{id}', response_model=IUser)
def get_specific_user(
    id: int, 
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(User).filter_by(id=id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with {id=} does not exists")

    return user
