from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.core.database import Base, engine
from app.models.user import User

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    health_router,
    prefix="/api/v1"
)