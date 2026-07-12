import json
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.advanced_repository import (
    AuditRepository,
    DeviceRepository,
    ShareRepository,
    StorageVolumeRepository,
    SyncRepository,
    UploadSessionRepository,
    VersionRepository
)
from app.repositories.file_repository import FileRepository
from app.repositories.folder_repository import FolderRepository
from app.services.security_service import MalwareScanner
from app.services.storage_service import StorageService
from app.storage.utils.file_utils import calculate_checksum
from app.core.config import settings


class AdvancedService:

    @staticmethod
    def _is_expired(expires_at: datetime):
        now = datetime.now(timezone.utc)

        if expires_at.tzinfo is None:
            now = now.replace(tzinfo=None)

        return expires_at < now

    @staticmethod
    def create_audit(
        db: Session,
        user_id: int | None,
        action: str,
        resource_type: str,
        resource_id: int | None = None,
        metadata: dict | None = None
        ):

        return AuditRepository.create_log(
            db,
            user_id,
            action,
            resource_type,
            resource_id,
            metadata
        )

    @staticmethod
    def list_audit_logs(db: Session, current_user: User):
        return AuditRepository.list_user_logs(db, current_user.id)

    @staticmethod
    def create_share(
        db: Session,
        file_id: int,
        current_user: User,
        shared_with_user_id: int | None,
        permission: str,
        expires_at: datetime | None
        ):

        file = FileRepository.get_user_file_by_id(
            db,
            file_id,
            current_user.id
        )

        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        share = ShareRepository.create_share(
            db,
            file_id,
            current_user.id,
            shared_with_user_id,
            permission,
            expires_at
        )
        AdvancedService.create_audit(
            db,
            current_user.id,
            "share_created",
            "file",
            file_id
        )
        return share

    @staticmethod
    def list_shares(db: Session, current_user: User):
        return ShareRepository.list_user_shares(db, current_user.id)

    @staticmethod
    def revoke_share(db: Session, share_id: int, current_user: User):
        shares = ShareRepository.list_user_shares(db, current_user.id)
        share = next((item for item in shares if item.id == share_id), None)

        if not share:
            raise HTTPException(status_code=404, detail="Share not found")

        return ShareRepository.revoke_share(db, share)

    @staticmethod
    def get_shared_file_download(db: Session, token: str):
        share = ShareRepository.get_active_by_token(db, token)

        if not share:
            raise HTTPException(status_code=404, detail="Share not found")

        file = FileRepository.get_by_id(db, share.file_id)

        if not file or not StorageService.provider.file_exists(file.storage_path):
            raise HTTPException(status_code=404, detail="File not found")

        return file, StorageService.provider.open_file(file.storage_path)

    @staticmethod
    def create_upload_session(
        db: Session,
        current_user: User,
        folder_id: int | None,
        original_filename: str,
        mime_type: str | None,
        total_size: int,
        chunk_size: int
        ):

        if folder_id is not None:
            folder = FolderRepository.get_active_user_folder_by_id(
                db,
                folder_id,
                current_user.id
            )
            if not folder:
                raise HTTPException(status_code=404, detail="Folder not found")

        if total_size <= 0 or chunk_size <= 0:
            raise HTTPException(status_code=400, detail="Invalid upload size")

        total_chunks = (total_size + chunk_size - 1) // chunk_size

        return UploadSessionRepository.create_session(
            db,
            current_user.id,
            folder_id,
            original_filename,
            mime_type,
            total_size,
            chunk_size,
            total_chunks
        )

    @staticmethod
    def upload_chunk(
        db: Session,
        current_user: User,
        session_id: int,
        chunk_index: int,
        chunk: UploadFile
        ):

        session = UploadSessionRepository.get_user_session(
            db,
            session_id,
            current_user.id
        )

        if not session or session.completed_at:
            raise HTTPException(status_code=404, detail="Upload session not found")

        if AdvancedService._is_expired(session.expires_at):
            raise HTTPException(status_code=410, detail="Upload session expired")

        if chunk_index < 0 or chunk_index >= session.total_chunks:
            raise HTTPException(status_code=400, detail="Invalid chunk index")

        StorageService.provider.save_upload_chunk(
            session_id,
            chunk_index,
            chunk.file
        )

        session = UploadSessionRepository.mark_chunk_received(
            db,
            session,
            chunk_index
        )

        return {
            "session_id": session.id,
            "received_chunks": json.loads(session.received_chunks_json),
            "total_chunks": session.total_chunks
        }

    @staticmethod
    def finalize_upload_session(
        db: Session,
        current_user: User,
        session_id: int
        ):

        session = UploadSessionRepository.get_user_session(
            db,
            session_id,
            current_user.id
        )

        if not session or session.completed_at:
            raise HTTPException(status_code=404, detail="Upload session not found")

        received = set(json.loads(session.received_chunks_json))
        expected = set(range(session.total_chunks))

        if received != expected:
            raise HTTPException(status_code=400, detail="Upload is incomplete")

        assembled = StorageService.provider.assemble_upload_chunks(
            session.id,
            session.total_chunks
        )

        MalwareScanner.scan_or_raise(
            StorageService.provider.get_temp_file_path(assembled),
            session.original_filename
        )

        with StorageService.provider.open_temp_file(assembled) as temp_file:
            checksum, file_size = calculate_checksum(temp_file)

        if file_size != session.total_size:
            StorageService.provider.delete_temp_file(assembled)
            raise HTTPException(status_code=400, detail="Upload size mismatch")

        storage_path = StorageService.provider.move_temp_to_final(
            assembled,
            session.original_filename
        )

        file = FileRepository.create_file(
            db,
            session.original_filename,
            storage_path,
            session.mime_type,
            file_size,
            current_user.id,
            session.folder_id,
            checksum
        )
        VersionRepository.create_version(
            db,
            file.id,
            storage_path,
            file_size,
            checksum
        )
        UploadSessionRepository.complete_session(db, session)
        SyncRepository.create_event(db, current_user.id, "created", "file", file.id)
        AdvancedService.create_audit(
            db,
            current_user.id,
            "chunked_upload_finalized",
            "file",
            file.id
        )
        return file

    @staticmethod
    def list_versions(db: Session, file_id: int, current_user: User):
        file = FileRepository.get_user_file_by_id(db, file_id, current_user.id)

        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        return VersionRepository.list_versions(db, file_id)

    @staticmethod
    def upload_new_version(
        db: Session,
        file_id: int,
        current_user: User,
        upload: UploadFile
        ):

        file = FileRepository.get_user_file_by_id(db, file_id, current_user.id)

        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        temp_filename = StorageService.provider.save_temp_file(
            upload.file,
            file.original_filename
        )
        try:
            MalwareScanner.scan_or_raise(
                StorageService.provider.get_temp_file_path(temp_filename),
                file.original_filename
            )
        except HTTPException:
            StorageService.provider.delete_temp_file(temp_filename)
            raise
        checksum, file_size = calculate_checksum(upload.file)
        storage_path = StorageService.provider.move_temp_to_final(
            temp_filename,
            file.original_filename
        )
        version = VersionRepository.create_version(
            db,
            file.id,
            storage_path,
            file_size,
            checksum
        )
        SyncRepository.create_event(db, current_user.id, "versioned", "file", file.id)
        AdvancedService.create_audit(
            db,
            current_user.id,
            "version_uploaded",
            "file",
            file.id,
            {"version": version.version_number}
        )
        return version

    @staticmethod
    def download_version(
        db: Session,
        file_id: int,
        version_number: int,
        current_user: User
        ):

        file = FileRepository.get_user_file_by_id(db, file_id, current_user.id)
        version = VersionRepository.get_version(db, file_id, version_number)

        if not file or not version:
            raise HTTPException(status_code=404, detail="Version not found")

        return version, StorageService.provider.open_file(version.storage_path)

    @staticmethod
    def register_device(
        db: Session,
        current_user: User,
        client_id: str,
        name: str
        ):

        return DeviceRepository.upsert_device(db, current_user.id, client_id, name)

    @staticmethod
    def list_devices(db: Session, current_user: User):
        return DeviceRepository.list_devices(db, current_user.id)

    @staticmethod
    def list_sync_events(db: Session, current_user: User, after_id: int):
        return SyncRepository.list_events_after(db, current_user.id, after_id)

    @staticmethod
    def resolve_conflict(
        db: Session,
        current_user: User,
        file_id: int,
        client_checksum: str
        ):

        file = FileRepository.get_user_file_by_id(db, file_id, current_user.id)

        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        return {
            "file_id": file.id,
            "server_checksum": file.checksum,
            "client_checksum": client_checksum,
            "has_conflict": file.checksum != client_checksum,
            "resolution": "download_server_version" if file.checksum != client_checksum else "in_sync"
        }

    @staticmethod
    def create_storage_volume(db: Session, name: str, path: str):
        return StorageVolumeRepository.create_volume(db, name, path)

    @staticmethod
    def list_storage_volumes(db: Session):
        return StorageVolumeRepository.list_volumes(db)

    @staticmethod
    def consistency_report(db: Session, current_user: User):
        db_files = FileRepository.get_all_non_permanent_user_files(
            db,
            current_user.id
        )
        db_paths = {file.storage_path for file in db_files}
        disk_paths = set(StorageService.provider.list_storage_files())

        return {
            "missing_physical_files": [
                file.id
                for file in db_files
                if file.storage_path not in disk_paths
            ],
            "orphan_storage_paths": sorted(disk_paths - db_paths)
        }

    @staticmethod
    def cleanup_orphan_files(db: Session, current_user: User):
        report = AdvancedService.consistency_report(db, current_user)
        removed = []

        for storage_path in report["orphan_storage_paths"]:
            StorageService.provider.delete_file(storage_path)
            removed.append(storage_path)

        return {
            "removed": removed
        }

    @staticmethod
    def cleanup_expired_upload_sessions(db: Session, current_user: User):
        temp_files = StorageService.provider.list_temp_files()
        chunk_files = [
            path
            for path in temp_files
            if path.startswith("chunks/")
        ]

        return {
            "tracked_temp_files": temp_files,
            "chunk_files": chunk_files
        }

    @staticmethod
    def generate_thumbnail(
        db: Session,
        current_user: User,
        file_id: int
        ):

        file = FileRepository.get_user_file_by_id(
            db,
            file_id,
            current_user.id
        )

        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        if not file.mime_type or not file.mime_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Thumbnails are only supported for images"
            )

        try:
            from PIL import Image
        except ImportError as exc:
            raise HTTPException(
                status_code=500,
                detail="Pillow is required for thumbnail generation"
            ) from exc

        output = BytesIO()

        with StorageService.provider.open_file(file.storage_path) as source:
            image = Image.open(source)
            image.thumbnail(
                (settings.THUMBNAIL_MAX_SIZE, settings.THUMBNAIL_MAX_SIZE)
            )
            image.convert("RGB").save(output, format="JPEG", quality=85)

        output.seek(0)
        thumbnail_path = StorageService.provider.save_thumbnail(
            file.storage_path,
            output
        )
        AdvancedService.create_audit(
            db,
            current_user.id,
            "thumbnail_generated",
            "file",
            file.id,
            {"thumbnail_path": thumbnail_path}
        )

        return {
            "file_id": file.id,
            "thumbnail_path": thumbnail_path
        }
