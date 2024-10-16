from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from app import schemas
from .. import models
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix= "/votes",
    tags= ["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def post_vote(vote: schemas.PostVote, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    
    post_present_check = db.query(models.Post).filter(vote.post_id == models.Post.id)
    post = post_present_check.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Post with {vote.post_id} does not exist')
    post_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    found_vote = post_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Post with {vote.post_id} was already voted by user with {current_user.id}')
        else:
            vote_success = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(vote_success)
            db.commit()
            return {'message': 'Voted successfully'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Post with {vote.post_id} does not exist')
        else:
            post_query.delete(synchronize_session=False)
            db.commit()
            return {'message': 'Vote removed successfully'}

        
