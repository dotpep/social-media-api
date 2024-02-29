def test_successfully_delete_vote(authorized_client, test_posts, test_vote):
    post_id = test_posts[3].id
    is_vote = False  # if false then delete vote
    request_data = {"post_id": post_id, "is_voted": is_vote}
    
    res = authorized_client.post(f'/votes', json=request_data)
    vote = res.json()
    
    assert vote['message'] == 'successfully deleted vote'
    assert res.status_code == 201


def test_delete_non_exist_vote(authorized_client, test_posts):
    post_id = test_posts[3].id
    is_vote = False
    request_data = {"post_id": post_id, "is_voted": is_vote}
    
    res = authorized_client.post(f'/votes', json=request_data)
    vote = res.json()
    
    assert vote['detail'] == 'vote does not exists'
    assert res.status_code == 404