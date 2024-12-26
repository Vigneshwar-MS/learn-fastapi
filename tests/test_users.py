
import pytest
from app import schemas
# from .database import client, session
from app.config import settings
import jwt
from jsonschema import validate



def test_root(client):
    response = client.get("/")
    # print(response.json().get('message'))
    assert response.json()['message'] == 'Hello World'

def test_create_user(client):
    response = client.post("/users/", json={"email": "t4@test.com", "password":"1234"})
    new_user = schemas.UserResponse(**response.json())
    # print(type(new_user))
    expected_schema = {
  "title": "UserResponse",
  "type": "object",
  "properties": {
    "created_at": {
      "title": "Created At",
      "type": "string",
      "format": "date-time"
    },
    "id": {
      "title": "Id",
      "type": "integer"
    },
    "email": {
      "title": "Email",
      "type": "string",
      "format": "email"
    }
    
  },
  "required": ["id", "email", "created_at"]
}
    # We can also use validate method from jsonschema library to validate schema in addition to the validation using pydantic models implemented above
    # validate(instance=response.json(), schema=schemas.UserResponse.model_json_schema())
    
    # We can also use validate method from jsonschema library to validate schema using the expected schema defined above
    validate(instance=response.json(), schema=expected_schema)
    
    assert new_user.email == "t4@test.com"

def test_login_user(client, user_create):
    response = client.post("/login", data={"username":user_create['email'], "password": user_create['password']})
    assert response.status_code == 200
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    # print(type(payload))
    assert payload.get('user_id') == user_create['id']
    assert login_res.token_type == 'bearer'

@pytest.mark.parametrize("email, password, status_code", [
  ('wrongemail@test.com', '1234', 403),
  ('1@test.com', 'wrongpassword', 403),
  ('wrongemail@test.com', 'wrongpassword', 403),
  (None, '1234', 403),
  ('1@test.com', None, 403)
])
def test_incorrect_login(client, user_create, email, password, status_code):
  response = client.post("/login", data={"username":email, "password": password})
  assert response.status_code == status_code

    