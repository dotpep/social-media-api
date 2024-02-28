from app import schemas

from .database import (
    client,  # client fixture Depends on session (database fixture)
    session
)


def test_root(client):
    res = client.get('/root')
    print(type(res.json()))
    print(res.json().get('message'))
    print(res.status_code)
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users', json={'email': 'foo@bar.com', 'password': 'password1234'})
    #print(res.json())
    
    new_user = schemas.User(**res.json())
    
    assert res.status_code == 201
    assert new_user.email == 'foo@bar.com'
    
    #data = res.json()
    #assert data.get('email') == 'foo@bar.com'
    #assert "id" in data
