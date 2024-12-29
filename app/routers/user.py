from app import schemas
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from app.utils import hash_password
from app import models
from app.database import get_db

router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user_data = models.User(email = user.email, password = hashed_password)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data

@router.get("/{id}", status_code= status.HTTP_200_OK, response_model= schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The user with {id} does not exist")
    return user