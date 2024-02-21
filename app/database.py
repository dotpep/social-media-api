from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time

# 'postgresql://<username>:<password>@<ip-address/hostname:port>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## Connect postgres DB
#while True:
#    try:
#        conn = psycopg2.connect(
#            dbname="social_media_fastapi",
#            user="postgres",
#            password="1234",
#            host="localhost",
#            port="5432",
#            cursor_factory=RealDictCursor
#        )
#        cursor = conn.cursor()
#        print("Database connection was established successfully!")
#        break
#    except Exception as error:
#        print("Failed to connect database!")
#        print("Exception Error: ", error)
#        time.sleep(10)
