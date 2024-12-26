
import pytest
from app import schemas
from app.config import settings
from jsonschema import validate

def test_get_all_posts(authorized_client, insert_post_data_in_db):
    res = authorized_client.get('/posts/')
    assert res.status_code == 200
    assert len(res.json()) == len(insert_post_data_in_db)
    def validate_schema(post):
        return schemas.PostResponse(**post)
    
    posts_map = map(validate_schema, res.json())
    # posts = list(posts_map)
    # print(posts)
    # print('----------------')
    # print(res.json())
    
def test_unauthorized_user_get_post(client, insert_post_data_in_db):
    res = client.get('/posts/')
    assert res.status_code == 401
    

def test_unauthorized_user_get_one_post(client, insert_post_data_in_db):
    res = client.get(f'/posts/{insert_post_data_in_db[0].id}')
    assert res.status_code == 401
    

def test_authorized_user_get_unavailable_post(authorized_client):
    res = authorized_client.get(f'/posts/234983271498237')
    assert res.status_code == 404
    
  
def test_authorized_user_get_one_post(authorized_client, insert_post_data_in_db):
    res = authorized_client.get(f'/posts/{insert_post_data_in_db[0].id}')
    assert res.status_code == 200
    
def test_authorized_user_create_post(authorized_client, user_create):
    res = authorized_client.post('/posts/', json={'title' : 'First Title', 'genre' : 'Comedy', 'ott_release' : True, 'rating' : 5, 'owner_id' : user_create['id']})
    assert res.status_code == 201


def test_unauthorized_user_create_post(client, user_create):
    res = client.post('/posts/', json={'title' : 'First Title', 'genre' : 'Comedy', 'ott_release' : True, 'rating' : 5, 'owner_id' : user_create['id']})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, insert_post_data_in_db):
    res = client.delete(f'/posts/{insert_post_data_in_db[0].id}' )
    assert res.status_code == 401
    

def test_authorized_user_delete_post(authorized_client, insert_post_data_in_db):
    res = authorized_client.delete(f'/posts/{insert_post_data_in_db[0].id}' )
    assert res.status_code == 204    


def test_authorized_user_delete_nonexistent_post(authorized_client):
    res = authorized_client.delete('/posts/8498498')
    assert res.status_code == 404   

def test_authorized_user_delete_other_users_post(authorized_client, insert_post_data_in_db):
    res = authorized_client.delete(f'/posts/{insert_post_data_in_db[3].id}' )
    assert res.status_code == 401


def test_unauthorized_user_update_post(client, insert_post_data_in_db):
    data = {'title' : 'Updated Title', 'ott_release' : False}
    
    res = client.put(f'/posts/{insert_post_data_in_db[0].id}', json = data)
    assert res.status_code == 401


def test_authorized_user_update_post(authorized_client, insert_post_data_in_db):
    data = {'title' : 'Updated Title', 'genre': 'Horror', 'ott_release' : False}
    
    res = authorized_client.put(f'/posts/{insert_post_data_in_db[0].id}', json = data)
    assert res.status_code == 200
    
def test_authorized_user_update_another_user_post(authorized_client, insert_post_data_in_db):
    data = {'title' : 'Updated Title', 'genre': 'Horror', 'ott_release' : False}
    
    res = authorized_client.put(f'/posts/{insert_post_data_in_db[3].id}', json = data)
    assert res.status_code == 401


def test_authorized_user_update_nonexistent_post(authorized_client):
    data = {'title' : 'Updated Title', 'genre': 'Horror', 'ott_release' : False}
    
    res = authorized_client.put('/posts/9090909', json = data)
    assert res.status_code == 404
    

