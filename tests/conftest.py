from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import get_db, Base
from .database import TestingSessionLocal, engine


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
@pytest.fixture
def test_user(client):
    user_data = {'email': 'test_user@gmail.com', 
                 'password': 'password1234'}
    res = client.post('/users', json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
