import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    youtube_api_key: str
    evolution_api_url: str
    evolution_api_token: str
    evolution_instance: str
    whatsapp_recipient: str  # Format: "919876543210@s.whatsapp.net" or phone number depending on instance style

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

def get_settings() -> Settings:
    return Settings(
        youtube_api_key=os.getenv("YOUTUBE_API_KEY", ""),
        evolution_api_url=os.getenv("EVOLUTION_API_URL", ""),
        evolution_api_token=os.getenv("EVOLUTION_API_TOKEN", ""),
        evolution_instance=os.getenv("EVOLUTION_INSTANCE", ""),
        whatsapp_recipient=os.getenv("WHATSAPP_RECIPIENT", "")
    )