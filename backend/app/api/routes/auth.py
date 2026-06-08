from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest
)
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
    ):
    user = AuthService.register(
        db,
        payload.email,
        payload.password
    )

    return {
        "id": user.id,
        "email": user.email
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
    ):

    return AuthService.login(
        db,
        payload.email,
        payload.password
    )

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
    ):

    return {
        "id": current_user.id,
        "email": current_user.email
    }