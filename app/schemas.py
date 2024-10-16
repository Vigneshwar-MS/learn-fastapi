from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    genre: str
    ott_release : bool = True # If the user does not provide the value, the default value will be taken as True
    rating: Optional[int] = None # If the user does not provide the value, no value will be assigned to rating since it is an optional field

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True

class PostVoteResponse(PostResponse):
    # post: PostResponse
    votes: int
    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class PostVote(BaseModel):
    post_id: int
    dir: int