# config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    model: str = "gpt-4-turbo-preview"

    access_token: str
    recipient_waid: str
    phone_number_id: str
    version: str = "v19.0"
    app_id: str
    app_secret: str
    verify_token: str

    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
