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
