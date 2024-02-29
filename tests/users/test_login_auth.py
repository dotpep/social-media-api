import pytest
from jose import jwt

from app.config import settings
from app import schemas


def test_login_user(client, test_user):
    request_data = {'username': test_user['email'], 'password': test_user['password']}
    
    res = client.post('/login', data=request_data)
    user = res.json()
    
    login_resp = schemas.Token(**user)
    paylaod = jwt.decode(login_resp.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = paylaod.get("user_id")

    assert user_id == test_user['id']
    assert login_resp.access_token == user['access_token']
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
    request_data = {'username': email, 'password': password}
    
    res = client.post('/login', data=request_data)
    
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'
