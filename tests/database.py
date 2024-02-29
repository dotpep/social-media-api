from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
import testing.postgresql

from app.config import settings


# Database will be created and deleted automatically when you run pytests

# Setup the postgres_test database for testing
# You can connect to database as normal with dbname_test, query, see tables, records etc. When test is fail
DATABASE_NAME = f'{settings.DATABASE_NAME}_test'
NORMAL_PSQL_DB_URL = f'postgresql+psycopg2://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{DATABASE_NAME}'

# Create database if not already created
if not database_exists(NORMAL_PSQL_DB_URL):
    create_database(NORMAL_PSQL_DB_URL)


# Setup temporary testing postgres database
postgresql = testing.postgresql.Postgresql()
TEMP_PSQL_DB_URL = postgresql.url()


# Change engine NORMAL_PSQL_DB_URL or TEMP_PSQL_DB_URL
# In NORMAL_PSQL_DB_URL you can connect to database and it creates Normal database
# In TEMP_PSQL_DB_URL you cannot connect to database but it creates Temporary database
engine = create_engine(NORMAL_PSQL_DB_URL)


# Make Testing Session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
