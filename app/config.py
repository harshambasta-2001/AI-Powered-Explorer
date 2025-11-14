import boto3
from pydantic_settings import BaseSettings
import subprocess


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_DAYS:int
    MCP_SEARCH_URL:str
    MCP_IMAGE_URL:str


    class Config:
        env_file = ".env"


settings = Settings()
