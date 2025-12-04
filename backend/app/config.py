import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./snake_arena.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production-please"
    algorithm: str = "HS256"
    access_token_expire_days: int = 7
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()
