import pytest

from app import schemas


@pytest.mark.parametrize('title, content, published', [
    ("first updated post title", "update some content", False),
    ("updated post title", "some updated post content", True),
    ("another updated post title", "another updated post content", False),
])
def test_user_successfully_update_post(authorized_client, test_user, test_posts, title, content, published):
    test_post = test_posts[0]
    post_id = test_post.id
    request_data = {"title": title, 
                    "content": content, 
                    "published": published}
    
    res = authorized_client.put(f'/posts/{post_id}', json=request_data)
    post = res.json()
    
    validated_updated_post = schemas.Post(**post)
    
    assert validated_updated_post.id == post_id
    assert validated_updated_post.title == test_post.title
    assert validated_updated_post.content == test_post.content
    assert validated_updated_post.published == test_post.published
    assert validated_updated_post.owner_id == test_user['id']
    
    assert res.status_code == 200



def test_update_post_non_exist(authorized_client, test_user, test_posts):
    post_id = 9999
    request_data = {"title": "first try to update post title", 
                    "content": "updated content", 
                    "published": False}
    res = authorized_client.put(f'/posts/{post_id}', json=request_data)

    assert res.status_code == 404


@pytest.mark.parametrize('title, content, published', [
    ("first try to update post title", "updated content", False),
    ("another updated post title", "another updated post content", False),
])
def test_update_other_user_post(authorized_client, test_user, test_posts, title, content, published):
    test_post = test_posts[3]
    another_user_post_id = test_post.id
    request_data = {"title": title, 
                    "content": content, 
                    "published": published}
    
    res = authorized_client.put(f'/posts/{another_user_post_id}', json=request_data)
    
    assert test_post.title != title
    assert test_post.content != content
    assert test_post.published != published
    
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    post_id = test_posts[0].id
    request_data = {"title": "first try to update post title", 
                    "content": "updated content", 
                    "published": False}
    
    res = client.put(f'/posts/{post_id}', json=request_data)
    assert res.status_code == 401