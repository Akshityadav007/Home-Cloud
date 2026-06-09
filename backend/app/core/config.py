from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    STORAGE_ROOT_PATH: str = "../storage/files"
    TEMP_STORAGE_PATH: str = "../storage/temp"

    class Config:
        env_file = ".env"

settings = Settings()