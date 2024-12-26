from fastapi.testclient import TestClient
import pytest
from app.database import get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base
from app.oauth2 import create_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL) 

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    

@pytest.fixture
def user_create(client):
    test_user_data = {"email": "1@test.com", "password":"1234"}
    response = client.post("/users", json=test_user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = test_user_data['password'] 
    # print(new_user)
    return new_user

@pytest.fixture
def user_create2(client):
    test_user_data = {"email": "2@test.com", "password":"1234"}
    response = client.post("/users", json=test_user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = test_user_data['password'] 
    # print(new_user)
    return new_user


@pytest.fixture
def token(user_create):
    return create_token({'user_id':user_create['id']})
    
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization':f'Bearer {token}'
                   }
    return client

@pytest.fixture
def insert_post_data_in_db(user_create, user_create2, session):
    post_data = [
        {'title' : 'First Title', 'genre' : 'Comedy', 'ott_release' : True, 'rating' : 5, 'owner_id' : user_create['id']},
        {'title' : 'Second Title', 'genre' : 'Black Comedy', 'ott_release' : False, 'rating' : 4, 'owner_id' : user_create['id']},
        {'title' : 'Third Title', 'genre' : 'Horror', 'ott_release' : True, 'rating' : 3, 'owner_id' : user_create['id']},
        {'title' : 'Fourth Title', 'genre' : 'Horror', 'ott_release' : True, 'rating' : 3, 'owner_id' : user_create2['id']}
    ]
    
    def create_post(post):
        return models.Post(**post)
        
        
    post_map = map(create_post, post_data)
    posts = list(post_map)
    session.add_all(posts);
    
    session.commit()
    get_posts = session.query(models.Post).all()
    return get_posts
