from fastapi import status

from app.schemas.user import IUser


def test_create_user(client):
    request_data = {'email': 'test_user@gmail.com', 'password': 'password1234'}
    
    res = client.post('/users', json=request_data)
    user = res.json()
    
    validated_new_user = IUser(**user)
    
    assert res.status_code == status.HTTP_201_CREATED
    assert validated_new_user.email == request_data['email']
    
    #data = res.json()
    #assert data.get('email') == 'foo@bar.com'
    #assert "id" in data
