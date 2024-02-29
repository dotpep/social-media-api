from app import schemas


def test_create_user(client):
    request_data = {'email': 'test_user@gmail.com', 'password': 'password1234'}
    
    res = client.post('/users', json=request_data)
    user = res.json()
    
    validated_new_user = schemas.User(**user)
    
    assert res.status_code == 201
    assert validated_new_user.email == request_data['email']
    
    #data = res.json()
    #assert data.get('email') == 'foo@bar.com'
    #assert "id" in data
