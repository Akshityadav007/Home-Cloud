from fastapi import (
    APIRouter,
    Depends,
    Query,
    UploadFile,
    File,
    Form
)
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.file import FileResponse
from app.services.file_service import (
    FileService
)
from typing import Optional
from fastapi.responses import StreamingResponse
from app.schemas.batch import (
    BatchFileOperationRequest,
    BatchDeleteResponse,
    BatchRestoreResponse,
    BatchPermanentDeleteResponse
)


router = APIRouter()


@router.get(
    "/",
    response_model=list[FileResponse]
)
def get_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.get_user_files(db, current_user)


# upload

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

@router.post(
    "/upload-multiple",
    response_model=list[FileResponse]
)
def upload_multiple_files(
        files: list[UploadFile] = File(...),
        folder_id: Optional[int] = Form(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):

    return FileService.upload_multiple_files(
        db=db,
        files=files,
        current_user=current_user,
        folder_id=folder_id
    )


# archive download

@router.post("/download-archive")
def download_archive(
    request: BatchFileOperationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    archive = FileService.get_archive_download(
        db,
        request.file_ids,
        current_user
    )

    return StreamingResponse(
        archive,
        media_type="application/zip",
        headers={
            "Content-Disposition":
            'attachment; filename="home-cloud-files.zip"'
        }
    )


# search

@router.get(
    "/search",
    response_model=list[FileResponse]
)
def search_files(
    q: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.search_files(db, current_user, q)


# delete and recovery

@router.get(
    "/trash",
    response_model=list[FileResponse]
)
def get_deleted_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.get_deleted_files(db, current_user)

@router.post(
    "/batch-delete",
    response_model=BatchDeleteResponse
)
def batch_delete_files(
    request: BatchFileOperationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return FileService.batch_delete_files(
        db=db,
        file_ids=request.file_ids,
        current_user=current_user
    )

@router.post(
    "/batch-restore",
    response_model=BatchRestoreResponse
)
def restore_multiple_files(
    request: BatchFileOperationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.restore_multiple_files(
        db,
        request.file_ids,
        current_user
    )


@router.post(
    "/{file_id}/restore",
    response_model=FileResponse
)
def restore_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.restore_file(
        db,
        file_id,
        current_user
    )

@router.post(
    "/batch-permanent-delete",
    response_model=BatchPermanentDeleteResponse
)
def batch_permanently_delete_files(
    request: BatchFileOperationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.batch_permanently_delete_files(
        db,
        request.file_ids,
        current_user
    )

@router.post("/cleanup/permanent-deletes")
def cleanup_permanently_deleted_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.cleanup_permanently_deleted_files(
        db,
        current_user
    )

@router.post(
    "/{file_id}/permanent-delete",
    response_model=FileResponse
)
def permanently_delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return FileService.permanently_delete_file(
        db,
        file_id,
        current_user
    )



# download

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

    return FileService.delete_file(db, file_id, current_user)
