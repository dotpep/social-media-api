import pytest
from typing import List

from app import schemas


#@pytest.mark.parametrize("title, content, published", [
#    ("my testing post title", "some random post content", None),
#    ("another post title", "another post content", False),
#    ("default publised field post title", "another post content", True),
#])
#def test_create_post(authorized_client):
#    authorized_client.post('/posts', json={"title": "my testing post title",
#                                           "content": "some random post content",
#                                           "published": True})


# Get all posts
def test_get_posts_list(authorized_client, test_posts):
    res = authorized_client.get('/posts')

    posts = res.json()
    assert len(posts) == len(test_posts)
    
    order_by_post_id = lambda x: (x['Post']['id'], x['Post']['id'])
    sorted_posts = sorted(posts, key=order_by_post_id)
    
    for i in range(len(test_posts)):
        validated_post = schemas.PostVote(**sorted_posts[i])
        
        assert validated_post.Post.title == test_posts[i].title
        assert validated_post.Post.content == test_posts[i].content
        assert validated_post.Post.owner_id == test_posts[i].owner_id
        
    #    print(validated_posts)
    #    print("--------------------------------")
    #print("--------------------------------")

    #validated_posts = [schemas.PostVote(**sorted_posts[i]) for i in range(len(posts))]
    #print(validated_posts)
    #print("--------------------------------")
    
    #posts_validator = lambda post: schemas.PostVote(**post)
    #validated_posts_map = map(posts_validator, sorted_posts)
    #validated_posts = list(validated_posts_map)
    
    #print(validated_posts)
    
    #for i in range(len(test_posts)):
    #    assert validated_posts[i].Post.title == test_posts[i].title
    #    assert validated_posts[i].Post.content == test_posts[i].content
    #    assert validated_posts[i].Post.owner_id == test_posts[i].owner_id
    
    
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts')
    assert res.status_code == 401


# Get one specific post
def test_get_one_post_detail(authorized_client, test_posts):
    test_post = test_posts[0]
    post_id = test_post.id
    
    res = authorized_client.get(f'/posts/{post_id}')
    post = res.json()
    
    validated_post = schemas.PostVote(**post)
    
    assert validated_post.Post.id == post_id
    assert validated_post.Post.title == test_post.title
    assert validated_post.Post.content == test_post.content
    assert validated_post.Post.owner_id == test_post.owner_id
    
    assert res.status_code == 200


def test_unauthorized_user_get_one_post_detail(client, test_posts):
    post_id = test_posts[0].id
    res = client.get(f'/posts/{post_id}')
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    post_id = 9999
    res = authorized_client.get(f'/posts/{post_id}')
    assert res.status_code == 404


# Get last post
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
    
    assert res.status_code == 200


def test_unauthorized_user_get_last_post(client, test_posts):
    res = client.get(f'/posts/latest')
    assert res.status_code == 401



# Create a new post
@pytest.mark.parametrize("title, content, published", [
    ("my testing post title default=published", "some random post content", True),
    ("another post title", "another post content", False),
    ("publised field post title with provided published field", "another post content", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    request_data = {"title": title, "content": content, "published": published}
    
    res = authorized_client.post(f'/posts', json=request_data)
    post = res.json()
    
    validated_created_post = schemas.Post(**post)
    
    assert validated_created_post.title == title
    assert validated_created_post.content == content
    assert validated_created_post.published == published
    
    assert validated_created_post.owner_id == test_user['id']
    assert res.status_code == 201


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    title = "post title, default published"
    content = "some content"
    request_data = {"title": title, "content": content}

    res = authorized_client.post(f'/posts', json=request_data)
    post = res.json()
    
    validated_created_post = schemas.Post(**post)
    
    assert validated_created_post.published == True
    assert res.status_code == 201
    
    assert validated_created_post.title == title
    assert validated_created_post.content == content


def test_unauthorized_user_create_post(client, test_user, test_posts):
    request_data = {"title": "post title created unauthorized user", "content": "some content"}
    res = client.post('/posts', json=request_data)
    assert res.status_code == 401


# Update a post
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


# Delete a post
def test_user_successfully_delete_post(authorized_client, test_user, test_posts):
    post_id = test_posts[0].id
    res = authorized_client.delete(f'/posts/{post_id}')
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    post_id = 9999
    res = authorized_client.delete(f'/posts/{post_id}')
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    another_user_post_id = test_posts[3].id
    res = authorized_client.delete(f'/posts/{another_user_post_id}')
    assert res.status_code == 403


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    post_id = test_posts[0].id
    res = client.delete(f'/posts/{post_id}')
    assert res.status_code == 401
