from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    PROJECT_NAME: str = ""
    API_VERSION: str = ""
    BACKEND_CORS_ORIGINS: list[str] = []

    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_DATABASE: str
    MONGO_QUERY: str = "retryWrites=true&w=majority"

    @computed_field
    @property
    def MONGO_URI(self) -> str:
        return (
            f"mongodb+srv://"
            f"{self.MONGO_USER}"
            f":{self.MONGO_PASSWORD}"
            f"@{self.MONGO_HOST}/"
            f"?{self.MONGO_QUERY}"
        )
