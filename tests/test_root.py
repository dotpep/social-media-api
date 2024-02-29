from fastapi import status


def test_root(client):
    res = client.get('/root')
    #print(type(res.json()))
    #print(res.json().get('message'))
    #print(res.status_code)
    assert res is not None
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('message') == 'Hello World'
