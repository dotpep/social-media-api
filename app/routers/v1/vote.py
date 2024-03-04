from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models.vote import Vote
from app.models.post import Post
from app.schemas.user import IUser
from app.schemas.vote import Vote
from app.configs import database
from app.utils import oauth2


router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)


def add_vote():
    pass

def delete_vote():
    pass


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: Vote, 
    db: Session = Depends(database.get_db), 
    current_user: IUser = Depends(oauth2.get_current_user)
):
    post_id = vote.post_id
    user_id = current_user.id
    post = db.query(Post).filter_by(id=post_id).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {post_id=} was not found")
    
    
    vote_query = db.query(Vote).filter(
        Vote.post_id == post_id, 
        Vote.user_id == user_id)
    found_vote = vote_query.first()
    if vote.is_voted:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {user_id=} has already voted on post {post_id=}")

        new_vote = Vote(post_id=post_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exists")
            
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "successfully deleted vote"}
