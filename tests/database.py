from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


# Setup the postgres_test database for testing
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
