from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.folder import (
    CreateFolderRequest,
    FolderResponse
)
from app.services.folder_service import FolderService
from app.schemas.navigation import (
    FolderContentsResponse
)


router = APIRouter()


@router.post(
    "/",
    response_model=FolderResponse
)
def create_folder(
        payload: CreateFolderRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):

    return FolderService.create_folder(
        db=db,
        name=payload.name,
        current_user=current_user,
        parent_folder_id=payload.parent_folder_id
    )


@router.get(
    "/",
    response_model=list[FolderResponse]
)
def get_folders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FolderService.get_user_folders(
        db,
        current_user
    )

@router.get(
    "/root/contents",
    response_model=FolderContentsResponse
)
def get_root_contents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FolderService.get_root_contents(
        db,
        current_user
    )

@router.get(
    "/trash",
    response_model=list[FolderResponse]
)
def get_deleted_folders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FolderService.get_deleted_folders(
        db,
        current_user
    )


@router.get(
    "/{folder_id}/contents",
    response_model=FolderContentsResponse
)
def get_folder_contents(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FolderService.get_folder_contents(
        db,
        current_user,
        folder_id
    )


@router.post(
    "/{folder_id}/restore",
    response_model=FolderResponse
)
def restore_folder(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FolderService.restore_folder(
        db,
        folder_id,
        current_user
    )


@router.post(
    "/{folder_id}/permanent-delete",
    response_model=FolderResponse
)
def permanently_delete_folder(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FolderService.permanently_delete_folder(
        db,
        folder_id,
        current_user
    )


@router.delete("/{folder_id}")
def delete_folder(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FolderService.delete_folder(
        db,
        folder_id,
        current_user
    )
