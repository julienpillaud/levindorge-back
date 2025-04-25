from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    PROJECT_NAME: str
    API_VERSION: str
    BACKEND_CORS_ORIGINS: list[str] = []
