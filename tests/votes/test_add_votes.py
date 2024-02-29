from fastapi import status

from app import models


def test_vote_on_post(authorized_client, test_user, test_posts, session):
    test_post = test_posts[3]
    post_id = test_post.id
    user_id = test_user['id']
    
    request_data = {"post_id": post_id, "is_voted": True}
    
    res = authorized_client.post(f'/votes', json=request_data)
    vote = res.json()
    
    query_post = session.query(models.Post).filter_by(id=post_id).first()
    db_post_id = query_post.id
    
    query_user = session.query(models.User).filter_by(id=user_id).first()
    db_user_id = query_user.id
    
    query_vote = session.query(models.Vote).filter(models.Vote.post_id == db_post_id,
                                                   models.Vote.user_id == db_user_id).first()
    
    assert post_id == db_post_id
    assert user_id == db_user_id
    
    assert db_post_id == query_vote.post_id
    assert db_user_id == query_vote.user_id
    
    assert vote['message'] == 'successfully added vote'
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_twice_post(authorized_client, test_posts, test_vote, test_user):
    post_id = test_posts[3].id
    is_vote = True  # if true then add vote
    
    user_id = test_user['id']
    
    request_data = {"post_id": post_id, "is_voted": is_vote}
    res = authorized_client.post(f'/votes', json=request_data)
    vote = res.json()
    
    assert vote['detail'] == f"user {user_id=} has already voted on post {post_id=}"
    assert res.status_code == status.HTTP_409_CONFLICT



def test_vote_non_exist_post(authorized_client, test_posts):
    post_id = 999999
    is_vote = True
    request_data = {"post_id": post_id, "is_voted": is_vote}
    
    res = authorized_client.post(f'/votes', json=request_data)
    vote = res.json()
    
    assert vote['detail'] == f"post with {post_id=} was not found"
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_user_vote_on_post(client, test_posts):
    post_id = test_posts[3].id
    is_vote = True
    request_data = {"post_id": post_id, "is_voted": is_vote}
    
    res = client.post('/votes', json=request_data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
