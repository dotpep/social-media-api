import pytest
from jose import jwt

from app.config import settings
from app import schemas


#@app.get('/root', tags=["Welcome Home Page"], status_code=200)
#def root():
#    return {"message": "Hello World"}

#def test_root(client):
#    res = client.get('/root')
#    print(type(res.json()))
#    print(res.json().get('message'))
#    print(res.status_code)
#    assert res.json().get('message') == 'Hello World'
#    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users', json={'email': 'test_user@gmail.com', 'password': 'password1234'})
    #print(res.json())
    
    new_user = schemas.User(**res.json())
    
    assert res.status_code == 201
    assert new_user.email == 'test_user@gmail.com'
    
    #data = res.json()
    #assert data.get('email') == 'foo@bar.com'
    #assert "id" in data


def test_login_user(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 
                                      'password': test_user['password']})
    
    login_resp = schemas.Token(**res.json())
    paylaod = jwt.decode(login_resp.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = paylaod.get("user_id")
    
    assert id == test_user['id']
    assert login_resp.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@email.com', 'password1234', 403),
    ('test_user@gmail.com', 'wrongpassword1234', 403),
    ('wrong@email.com', 'wrongpassword1234', 403),
    (None, 'password1234', 422),
    ('wrong@email.com', None, 422),
    (None, None, 422),
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post('/login', data={'username': email, 
                                      'password': password})
    
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'
