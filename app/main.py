

from fastapi import FastAPI

from app.routers import vote
# from random import randrange
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, post, login

app = FastAPI()


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# def findPostById(id):
#     for post in my_posts:
#         if(post['id'] == int(id)):
#             return post;

# def find_index_of_post(id):
#     for index, post in enumerate(my_posts):
#         if(post['id'] == id):
#             return index;

# my_posts = [{"title": "My first title", "genre": "Horror", "ott_release" : True, "rating": 4, "id": 1}, {"title": "My second title", "genre": "Comedy", "rating": 5, "ott_release": False, "id": 2}]

app.include_router(user.router)
app.include_router(post.router)
app.include_router(login.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "bro"}


