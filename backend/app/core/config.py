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
    RATE_LIMIT_REQUESTS: int = 120
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    UPLOAD_SESSION_TTL_HOURS: int = 24
    BLOCKED_UPLOAD_EXTENSIONS: str = ".exe,.bat,.cmd,.ps1,.scr,.vbs,.js"
    CLAMSCAN_PATH: str = ""
    REQUIRE_STRONG_JWT_SECRET: bool = False
    THUMBNAIL_MAX_SIZE: int = 256

settings = Settings()
