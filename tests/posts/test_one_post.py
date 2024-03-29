from fastapi import status

from app.schemas.post import IPostVote


def test_get_one_post_detail(authorized_client, test_posts):
    test_post = test_posts[0]
    post_id = test_post.id
    
    res = authorized_client.get(f'/posts/{post_id}')
    post = res.json()
    
    validated_post = IPostVote(**post)
    
    assert validated_post.Post.id == post_id
    assert validated_post.Post.title == test_post.title
    assert validated_post.Post.content == test_post.content
    assert validated_post.Post.owner_id == test_post.owner_id
    
    assert res.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_one_post_detail(client, test_posts):
    post_id = test_posts[0].id
    res = client.get(f'/posts/{post_id}')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_not_exist(authorized_client, test_posts):
    post_id = 9999
    res = authorized_client.get(f'/posts/{post_id}')
    assert res.status_code == status.HTTP_404_NOT_FOUND