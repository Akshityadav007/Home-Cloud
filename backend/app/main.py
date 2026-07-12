from fastapi import FastAPI
from app.api.routes.health import router as health_router
# from app.core.database import Base, engine
# from app.models.user import User
from app.api.routes.auth import router as auth_router
from app.api.routes.folders import (
    router as folder_router
)
from app.api.routes.files import (
    router as file_router
)
from app.api.routes.advanced import (
    router as advanced_router
)
from app.core.config import settings
from app.services.security_service import RateLimitMiddleware

# Base.metadata.create_all(bind=engine)

app = FastAPI()

if settings.REQUIRE_STRONG_JWT_SECRET and settings.JWT_SECRET_KEY == "change-me-in-production":
    raise RuntimeError("JWT_SECRET_KEY must be changed for production")

app.add_middleware(RateLimitMiddleware)

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth"
)

app.include_router(
    folder_router,
    prefix="/api/v1/folders"
)

app.include_router(
    file_router,
    prefix="/api/v1/files"
)

app.include_router(
    advanced_router,
    prefix="/api/v1"
)
