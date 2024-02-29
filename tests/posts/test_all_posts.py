from fastapi import status

from app import schemas


def test_get_posts_list(authorized_client, test_posts):
    res = authorized_client.get('/posts')

    posts = res.json()
    
    QUERY_PARAM_PAGINATE_LIMIT: int = 5
    assert len(posts) <= QUERY_PARAM_PAGINATE_LIMIT
    
    order_by_post_id = lambda x: (x['Post']['id'], x['Post']['id'])
    sorted_posts = sorted(posts, key=order_by_post_id)
    
    for i in range(len(posts)):
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
    
    #for i in range(len(posts)):
    #    assert validated_posts[i].Post.title == test_posts[i].title
    #    assert validated_posts[i].Post.content == test_posts[i].content
    #    assert validated_posts[i].Post.owner_id == test_posts[i].owner_id
    
    
    assert res.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
