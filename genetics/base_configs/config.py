from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPEN_API_KEY: str

    POSTGRES_URL: str

    QDRANT_URL: str

    class Config:
        env_file = ".env"


settings = Settings()