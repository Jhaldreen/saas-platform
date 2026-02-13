from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_EXPIRATION: int

    class Config:
        env_file = ".env"

settings = Settings()