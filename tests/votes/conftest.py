import pytest

from app.models.vote import Vote


@pytest.fixture
def test_vote(test_user, test_posts, session):
    post_id = test_posts[3].id
    new_vote = Vote(post_id=post_id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()