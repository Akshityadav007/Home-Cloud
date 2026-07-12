from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "sqlite:///./home_cloud.db"
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    STORAGE_ROOT_PATH: str = "storage/files"
    TEMP_STORAGE_PATH: str = "storage/temp"
    MAX_UPLOAD_SIZE_BYTES: int = 0
    USER_STORAGE_QUOTA_BYTES: int = 0

settings = Settings()
