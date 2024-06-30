from pydantic_settings import BaseSettings
from pydantic import ValidationError

class Settings(BaseSettings):
    api_id: int
    api_hash: str
    bot_token: str
    download_path: str
    rate_limit: float  # Rate limit in seconds
    url: str

    class Config:
        env_file = '.env'

try:
    settings = Settings()
except ValidationError as e:
    print("Environment variables are not set correctly:", e)
    exit(1)
