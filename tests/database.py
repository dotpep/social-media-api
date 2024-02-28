from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


from app.main import app
from app.config import settings
from app.database import get_db, Base


# Setup the postgres_test database for testing
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    """Database fixture to drop and return new TestingSession"""
    # Create and Drop table in Database when using client fixture
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Setup the Test Database SQLAlchemy Session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
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
