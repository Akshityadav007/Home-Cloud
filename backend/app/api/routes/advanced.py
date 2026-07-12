from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.models.user import User
from app.schemas.advanced import (
    AuditLogResponse,
    ConflictRequest,
    CreateShareRequest,
    CreateUploadSessionRequest,
    DeviceRequest,
    DeviceResponse,
    FileVersionResponse,
    ShareResponse,
    StorageVolumeRequest,
    UploadSessionResponse
)
from app.schemas.file import FileResponse
from app.services.advanced_service import AdvancedService


router = APIRouter()


@router.get("/audit", response_model=list[AuditLogResponse])
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.list_audit_logs(db, current_user)


@router.post("/files/{file_id}/shares", response_model=ShareResponse)
def create_share(
    file_id: int,
    request: CreateShareRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.create_share(
        db,
        file_id,
        current_user,
        request.shared_with_user_id,
        request.permission,
        request.expires_at
    )


@router.get("/shares", response_model=list[ShareResponse])
def list_shares(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.list_shares(db, current_user)


@router.post("/shares/{share_id}/revoke", response_model=ShareResponse)
def revoke_share(
    share_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.revoke_share(db, share_id, current_user)


@router.get("/shared/{token}/download")
def download_shared_file(
    token: str,
    db: Session = Depends(get_db)
    ):

    file, file_stream = AdvancedService.get_shared_file_download(db, token)

    return StreamingResponse(
        file_stream,
        media_type=file.mime_type,
        headers={
            "Content-Disposition":
            f'attachment; filename="{file.original_filename}"'
        }
    )


@router.post("/uploads/sessions", response_model=UploadSessionResponse)
def create_upload_session(
    request: CreateUploadSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.create_upload_session(
        db,
        current_user,
        request.folder_id,
        request.original_filename,
        request.mime_type,
        request.total_size,
        request.chunk_size
    )


@router.post("/uploads/sessions/{session_id}/chunks/{chunk_index}")
def upload_chunk(
    session_id: int,
    chunk_index: int,
    chunk: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.upload_chunk(
        db,
        current_user,
        session_id,
        chunk_index,
        chunk
    )


@router.post(
    "/uploads/sessions/{session_id}/finalize",
    response_model=FileResponse
)
def finalize_upload_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.finalize_upload_session(
        db,
        current_user,
        session_id
    )


@router.get(
    "/files/{file_id}/versions",
    response_model=list[FileVersionResponse]
)
def list_versions(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.list_versions(db, file_id, current_user)


@router.post(
    "/files/{file_id}/versions",
    response_model=FileVersionResponse
)
def upload_new_version(
    file_id: int,
    upload: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.upload_new_version(
        db,
        file_id,
        current_user,
        upload
    )


@router.get("/files/{file_id}/versions/{version_number}/download")
def download_version(
    file_id: int,
    version_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    version, file_stream = AdvancedService.download_version(
        db,
        file_id,
        version_number,
        current_user
    )

    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition":
            f'attachment; filename="version-{version.version_number}"'
        }
    )


@router.post("/devices", response_model=DeviceResponse)
def register_device(
    request: DeviceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.register_device(
        db,
        current_user,
        request.client_id,
        request.name
    )


@router.get("/devices", response_model=list[DeviceResponse])
def list_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.list_devices(db, current_user)


@router.get("/sync/events")
def list_sync_events(
    after_id: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.list_sync_events(db, current_user, after_id)


@router.post("/sync/conflicts/resolve")
def resolve_conflict(
    request: ConflictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.resolve_conflict(
        db,
        current_user,
        request.file_id,
        request.client_checksum
    )


@router.post("/storage/volumes")
def create_storage_volume(
    request: StorageVolumeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.create_storage_volume(
        db,
        request.name,
        request.path
    )


@router.get("/storage/volumes")
def list_storage_volumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.list_storage_volumes(db)


@router.get("/storage/consistency")
def consistency_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.consistency_report(db, current_user)


@router.post("/storage/cleanup-orphans")
def cleanup_orphan_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.cleanup_orphan_files(db, current_user)


@router.post("/storage/cleanup-upload-sessions")
def cleanup_expired_upload_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.cleanup_expired_upload_sessions(db, current_user)


@router.post("/files/{file_id}/thumbnail")
def generate_thumbnail(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return AdvancedService.generate_thumbnail(db, current_user, file_id)
