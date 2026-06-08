from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.file import FileResponse
from app.services.file_service import (
    FileService
)
from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)
from typing import Optional
from fastapi.responses import StreamingResponse


router = APIRouter()


@router.get(
    "/",
    response_model=list[FileResponse]
)
def get_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.get_user_files(
        db,
        current_user
    )

@router.post(
    "/upload",
    response_model=FileResponse
)
def upload_file(
    file: UploadFile = File(...),
    folder_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.upload_file(
        db=db,
        file=file,
        current_user=current_user,
        folder_id=folder_id
    )

@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    file, file_stream = (
        FileService.get_file_download(
            db,
            file_id,
            current_user
        )
    )

    return StreamingResponse(
        file_stream,
        media_type=file.mime_type,
        headers={
            "Content-Disposition":
            f'attachment; filename="{file.original_filename}"'
        }
    )

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.delete_file(
        db,
        file_id,
        current_user
    )