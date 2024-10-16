from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 

class Post(BaseModel):
    title: str
    genre: str
    ott_release : bool = True # If the user does not provide the value, the default value will be taken as True
    rating: Optional[int] = None # If the user does not provide the value, no value will be assigned to rating since it is an optional field

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='admin', cursor_factory=RealDictCursor);
        cursor = conn.cursor()
        print('Database connection established')
        break
    except Exception as e:
        print('Database connection failed')
        print("Database Error : ", e)

def findPostById(id):
    for post in my_posts:
        if(post['id'] == int(id)):
            return post;

def find_index_of_post(id):
    for index, post in enumerate(my_posts):
        if(post['id'] == id):
            return index;

my_posts = [{"title": "My first title", "genre": "Horror", "ott_release" : True, "rating": 4, "id": 1}, {"title": "My second title", "genre": "Comedy", "rating": 5, "ott_release": False, "id": 2}]


@app.get("/")
def read_root():
    return {"Hello": "bro"}

@app.get("/posts")
def getPosts():
    cursor.execute(''' SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {'data': posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post : Post):
    cursor.execute('''INSERT INTO posts (title, genre, ott_release, rating) VALUES(%s, %s, %s, %s) RETURNING *''', (post.title, post.genre, str(post.ott_release), str(post.rating)))
    
    # The commit method will insert the data in to database and if this line is omitted, the data will not be inserted
    conn.commit()
    post = cursor.fetchone()
    return {"data" : post};

@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id)))
    post = cursor.fetchone()
    # post = findPostById(id);
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with the model id {id} was not found");
    return {"data" : post};
    

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id)))
    conn.commit()
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with the given id {id} does not exist");
    
    return Response(status_code=status.HTTP_204_NO_CONTENT);

@app.put("/posts/{id}", status_code= status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title= %s, genre= %s, ott_release= %s WHERE id= %s RETURNING *''', (post.title, post.genre, str(post.ott_release), str(id)))
    conn.commit()
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with the given id {id} does not exist");
    
    return {"data" : updated_post};


@app.get("/posts/recent/latest")
def get_latest_post():
    return {"data" : my_posts[len(my_posts) - 1]};


