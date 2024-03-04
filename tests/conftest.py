from fastapi.testclient import TestClient
import pytest

from app.models.post import Post
from app.main import app
from app.configs.database import get_db, Base
from app.utils.oauth2 import create_access_token
from .database import TestingSessionLocal, engine
from .helpers import create_new_user


# Configuration Fixtures
@pytest.fixture(scope="function")
def session():
    """Database fixture to drop and return new TestingSession"""
    print("my session fixture ran")
    # Create and Drop table in Database when using client fixture
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Setup the Test Database SQLAlchemy Session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#@pytest.fixture(scope="module")
@pytest.fixture(scope="function")
def client(session):
    """TestClient fixture that depends on session fixture"""
    # Dependency to override the get_db dependency in the main app
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    # Setup the TestClient
    yield TestClient(app)


# Fixture for testing
# User and Authentication
@pytest.fixture
def test_user(client) -> dict:
    user_data = {'email': 'test_user@gmail.com', 
                 'password': 'password1234'}
    return create_new_user(client, user_data['email'], user_data['password'])


@pytest.fixture
def test_user2(client) -> dict:
    user_data = {'email': 'second_test_user2@gmail.com', 
                 'password': 'password1234'}
    return create_new_user(client, user_data['email'], user_data['password'])


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# Post
@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]
    
    #test_user_posts = [{
    #    "title": f"{i} post title",
    #    "content": f"{i} post content",
    #    "owner_id": test_user['id']
    #} for i in range(1, 4)]
    
    #test_user2_posts = [{
    #    "title": f"{i} post title",
    #    "content": f"{i} post content",
    #    "owner_id": test_user2['id']
    #} for i in range(4, 7)]
    
    #all_posts = test_user_posts + test_user2_posts
    
    
    create_post_model = lambda post: Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    
    #session.add_all(
    #    models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #    models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
    #    models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])
    #)
    
    session.commit()
    
    posts = session.query(Post).all()
    return posts
