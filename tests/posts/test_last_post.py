from fastapi import status

from app import schemas


def test_get_last_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/latest')
    post = res.json()
    
    test_posts_length = len(test_posts)
    test_post = test_posts[test_posts_length - 1]
    
    validated_post = schemas.PostVote(**post)
    
    assert validated_post.Post.id == test_post.id
    assert test_posts_length == test_post.id
    
    assert validated_post.Post.title == test_post.title
    assert validated_post.Post.content == test_post.content
    
    assert res.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_last_post(client, test_posts):
    res = client.get(f'/posts/latest')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
