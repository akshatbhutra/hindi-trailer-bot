import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    youtube_api_key: str
    evolution_api_url: str
    evolution_api_key: str
    whatsapp_number: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

def get_settings() -> Settings:
    return Settings(
        youtube_api_key=os.getenv("YOUTUBE_API_KEY", ""),
        evolution_api_url=os.getenv("EVOLUTION_API_URL", ""),
        evolution_api_key=os.getenv("EVOLUTION_API_KEY", ""),
        whatsapp_number=os.getenv("WHATSAPP_NUMBER", "")
    )