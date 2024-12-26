import pytest
from app import schemas
from app import models

@pytest.fixture
def test_create_vote_in_db(authorized_client, session, insert_post_data_in_db, user_create):
    vote = models.Vote(post_id=insert_post_data_in_db[0].id, user_id= user_create['id'])
    session.add(vote)
    session.commit()
    
    
def test_post_vote(authorized_client, insert_post_data_in_db):
    res = authorized_client.post('/votes', json={'post_id': insert_post_data_in_db[0].id, 'dir': 1})
    assert res.status_code == 201
    
def test_vote_twice(authorized_client, insert_post_data_in_db, test_create_vote_in_db):
    res = authorized_client.post('/votes', json={'post_id': insert_post_data_in_db[0].id, 'dir': 1})
    assert res.status_code == 409
    
def test_remove_vote_on_post(authorized_client, insert_post_data_in_db, test_create_vote_in_db):
    res = authorized_client.post('/votes', json={'post_id': insert_post_data_in_db[0].id, 'dir': 0})
    assert res.status_code == 201
    
def test_unauthorized_vote_on_post(client, insert_post_data_in_db,):
    res = client.post('/votes', json={'post_id': insert_post_data_in_db[0].id, 'dir': 1})
    assert res.status_code == 401

def test_post_vote(authorized_client, insert_post_data_in_db):
    res = authorized_client.post('/votes', json={'post_id': insert_post_data_in_db[0].id, 'dir': 1})
    assert res.status_code == 201
    
def test_remove_vote_on_post_which_is_note_voted_before(authorized_client, insert_post_data_in_db):
    res = authorized_client.post('/votes', json={'post_id': insert_post_data_in_db[3].id, 'dir': 0})
    assert res.status_code == 404
    
def test_vote_on_post_nonexistent(authorized_client, insert_post_data_in_db):
    res = authorized_client.post('/votes', json={'post_id': 9000, 'dir': 1})
    assert res.status_code == 404
