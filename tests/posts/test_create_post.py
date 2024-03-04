import pytest
from fastapi import status

from app.schemas.post import IPost


@pytest.mark.parametrize("title, content, published", [
    ("my testing post title default=published", "some random post content", True),
    ("another post title", "another post content", False),
    ("publised field post title with provided published field", "another post content", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    request_data = {"title": title, "content": content, "published": published}
    
    res = authorized_client.post(f'/posts', json=request_data)
    post = res.json()
    
    validated_created_post = IPost(**post)
    
    assert validated_created_post.title == title
    assert validated_created_post.content == content
    assert validated_created_post.published == published
    
    assert validated_created_post.owner_id == test_user['id']
    assert res.status_code == status.HTTP_201_CREATED


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    title = "post title, default published"
    content = "some content"
    request_data = {"title": title, "content": content}

    res = authorized_client.post(f'/posts', json=request_data)
    post = res.json()
    
    validated_created_post = IPost(**post)
    
    assert validated_created_post.published == True
    assert res.status_code == status.HTTP_201_CREATED
    
    assert validated_created_post.title == title
    assert validated_created_post.content == content


def test_unauthorized_user_create_post(client, test_user, test_posts):
    request_data = {"title": "post title created unauthorized user", "content": "some content"}
    res = client.post('/posts', json=request_data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
