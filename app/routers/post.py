from typing import Optional

from sqlalchemy import func
from app import schemas
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter, Response
from app import models
from app.database import get_db
from app import oauth2

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"])

@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user), 
             limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).all()
    print('Hello bro')
    post_vote_list = []

    for post, votes in results:
        # Convert the Post object to a dictionary (assuming it's an SQLAlchemy model)
        post_dict = post.__dict__.copy()
        # Optionally remove SQLAlchemy internal state, if necessary
        post_dict.pop('_sa_instance_state', None)

        # Add the vote count to the dictionary
        post_dict['votes'] = votes

        # Append the result to the list
        post_vote_list.append(post_dict)

    return post_vote_list


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post : schemas.CreatePost, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post = models.Post(title = post.title, genre = post.genre, ott_release = post.ott_release, rating = post.rating, owner_id = current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}")
def get_post(id : int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id)))
    # post = cursor.fetchone()
    # post = findPostById(id);
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"The post with the model id {id} was not found")

    results = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # Unpack the result tuple (Post object, Votes count)
    post, votes = results

    # Convert the Post object to a dictionary
    post_dict = post.__dict__.copy()
    # Optionally remove SQLAlchemy internal state
    post_dict.pop('_sa_instance_state', None)

    # Add the vote count to the dictionary
    post_dict['votes'] = votes

    return post_dict    

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with the given id {id} does not exist")
    post = query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised to perform the delete operation")
    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code= status.HTTP_200_OK, response_model= schemas.PostResponse)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with the given id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised to perform the update operation")
    
    post_query.update(updated_post.model_dump(), synchronize_session= False)
    db.commit()
    return post
