from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # as default is nothing setup
    # for development pydantic use/read .env file in project base directory
    # but you can change this to system environment variable in your machine or server
    
    # Database
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    
    # JWT Token
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    
    # this is for development read `.env` file
    class Config:
        env_file = ".env"


settings = Settings()
