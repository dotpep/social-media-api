def create_new_user(client, email, password):
    user_data = {'email': email, 
                 'password': password}
    res = client.post('/users', json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = password
    return new_user
