import pytest
import tempfile
from pathlib import Path
import os

os.environ.setdefault(
    "DATABASE_URL",
    f"sqlite:///{Path(tempfile.gettempdir()) / 'home_cloud_test.db'}"
)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
os.environ["STORAGE_ROOT_PATH"] = str(
    Path(tempfile.gettempdir()) / "home_cloud_storage" / "files"
)
os.environ["TEMP_STORAGE_PATH"] = str(
    Path(tempfile.gettempdir()) / "home_cloud_storage" / "temp"
)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base
from app.api.dependencies.database import get_db


SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():

    db = TestingSessionLocal()

    try:

        yield db

    finally:

        db.close()


@pytest.fixture
def client():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = (
        override_get_db
    )

    with TestClient(app) as c:

        yield c

    app.dependency_overrides.clear()
