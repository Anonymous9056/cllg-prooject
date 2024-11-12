from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Suitcase"
    PROJECT_VERSION: str = "0.0.1"
    API_URL: str = "http://localhost:8000"
    WEBSITE_URL: str = "http://localhost:3000"
    SUPERTOKENS_CONNECTION_URI: str = "http://localhost:3567"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/legaldb"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Environment
    ENV: str = "development"
    
    # API Keys
    GROQ_API_KEY: str
    QDRANT_API_KEY: str
    HUGGINGFACEHUB_API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

