from functools import lru_cache

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Intus Windows AI Chatbot"
    debug: bool = True
    origins: list = [
        "http://localhost",
        "http://localhost:8080",
    ]
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str  # priority: OS (firstly), .env file (secondly)
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


# @lru_cache  # Uncomment to enable settings object to be created only once (the first time it's called).
def get_settings():
    return Settings()


settings = get_settings()
print(settings.openai_api_key)
templates = Jinja2Templates(directory="app/templates")
