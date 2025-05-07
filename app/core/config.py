import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Document Generator API"
    DEBUG: bool = True
    DOCS_URL: str = "/docs"
    API_PREFIX: str = "/api/v1"
    DEFAULT_OUTPUT_FORMAT: str = "pdf"
    TEMP_DIR: str = "/tmp"
    TEMPLATE_DIR: str = "/app/templates"
    GENERATED_DIR: str = "/app/generated"
    ALLOWED_FORMATS: list[str] = ["pdf", "docx", "xlsx"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()