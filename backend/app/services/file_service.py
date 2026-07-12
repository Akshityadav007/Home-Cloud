from fastapi import (
    HTTPException,
    UploadFile
)
from io import BytesIO
from pathlib import Path
import zipfile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.repositories.file_repository import FileRepository
from app.repositories.folder_repository import FolderRepository
from app.services.storage_service import StorageService
from app.storage.utils.file_utils import calculate_checksum


class FileService:

    @staticmethod
    def _safe_original_filename(filename: str | None) -> str:

        if not filename:
            return "uploaded-file"

        safe_name = Path(filename.replace("\\", "/")).name

        return safe_name or "uploaded-file"

    @staticmethod
    def upload_file(
        db: Session,
        file: UploadFile,
        current_user: User,
        folder_id: int | None
        ):

        if folder_id is not None:

            folder = FolderRepository.get_active_user_folder_by_id(
                db,
                folder_id,
                current_user.id
            )

            if not folder:

                raise HTTPException(
                    status_code=404,
                    detail="Folder not found"
                )

        original_filename = FileService._safe_original_filename(
            file.filename
        )

        temp_filename = (
            StorageService.provider.save_temp_file(
                file.file,
                original_filename
            )
        )

        checksum, file_size = (
            calculate_checksum(file.file)
        )

        if (
            settings.MAX_UPLOAD_SIZE_BYTES > 0
            and file_size > settings.MAX_UPLOAD_SIZE_BYTES
        ):
            StorageService.provider.delete_temp_file(temp_filename)
            raise HTTPException(
                status_code=413,
                detail="File exceeds maximum upload size"
            )

        used_storage = FileRepository.get_used_storage_bytes(
            db,
            current_user.id
        )

        if (
            settings.USER_STORAGE_QUOTA_BYTES > 0
            and used_storage + file_size > settings.USER_STORAGE_QUOTA_BYTES
        ):
            StorageService.provider.delete_temp_file(temp_filename)
            raise HTTPException(
                status_code=413,
                detail="User storage quota exceeded"
            )

        storage_path = (
            StorageService.provider.move_temp_to_final(
                temp_filename,
                original_filename
            )
        )

        saved_file = (
            FileRepository.create_file(
                db=db,
                original_filename=original_filename,
                storage_path=storage_path,
                mime_type=file.content_type,
                size_bytes=file_size,
                owner_id=current_user.id,
                folder_id=folder_id,
                checksum=checksum
            )
        )

        return saved_file

    @staticmethod
    def get_user_files(
        db: Session,
        current_user: User
        ):

        return FileRepository.get_user_files(
            db,
            current_user.id
        )

    @staticmethod
    def get_file_download(
        db: Session,
        file_id: int,
        current_user: User
        ):

        file = FileRepository.get_user_file_by_id(
            db,
            file_id,
            current_user.id
        )

        if not file:

            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        if not StorageService.provider.file_exists(
            file.storage_path
        ):

            raise HTTPException(
                status_code=404,
                detail="Physical file missing"
            )

        file_stream = (
            StorageService.provider.open_file(
                file.storage_path
            )
        )

        return file, file_stream

    @staticmethod
    def get_archive_download(
        db: Session,
        file_ids: list[int],
        current_user: User
        ):

        if not file_ids:
            raise HTTPException(
                status_code=400,
                detail="At least one file is required"
            )

        files = FileRepository.get_user_files_by_ids(
            db,
            file_ids,
            current_user.id
        )

        files_by_id = {
            file.id: file
            for file in files
        }

        missing = [
            file_id
            for file_id in file_ids
            if file_id not in files_by_id
        ]

        if missing:
            raise HTTPException(
                status_code=404,
                detail="One or more files were not found"
            )

        archive = BytesIO()
        used_names = set()

        with zipfile.ZipFile(
            archive,
            mode="w",
            compression=zipfile.ZIP_DEFLATED
        ) as zip_archive:
            for file_id in file_ids:
                file = files_by_id[file_id]

                if not StorageService.provider.file_exists(
                    file.storage_path
                ):
                    raise HTTPException(
                        status_code=404,
                        detail="Physical file missing"
                    )

                archive_name = file.original_filename
                stem = Path(archive_name).stem
                suffix = Path(archive_name).suffix
                counter = 1

                while archive_name in used_names:
                    archive_name = f"{stem} ({counter}){suffix}"
                    counter += 1

                used_names.add(archive_name)

                with StorageService.provider.open_file(
                    file.storage_path
                ) as file_stream:
                    zip_archive.writestr(
                        archive_name,
                        file_stream.read()
                    )

        archive.seek(0)

        return archive

    @staticmethod
    def delete_file(
        db: Session,
        file_id: int,
        current_user: User
        ):

        file = FileRepository.get_user_file_by_id(
            db,
            file_id,
            current_user.id
        )

        if not file:

            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        FileRepository.soft_delete_file(
            db,
            file
        )

        return {
            "message": "File deleted successfully"
        }

    @staticmethod
    def search_files(
        db: Session,
        current_user: User,
        query: str
        ):

        if not query.strip():

            raise HTTPException(
                status_code=400,
                detail="Search query cannot be empty"
            )

        return FileRepository.search_files(
            db,
            current_user.id,
            query
        )

    @staticmethod
    def upload_multiple_files(
        db: Session,
        files: list[UploadFile],
        current_user: User,
        folder_id: int | None
        ):

        uploaded_files = []

        for file in files:

            uploaded_file = (
                FileService.upload_file(
                    db=db,
                    file=file,
                    current_user=current_user,
                    folder_id=folder_id
                )
            )

            uploaded_files.append(uploaded_file)

        return uploaded_files

    @staticmethod
    def batch_delete_files(
        db: Session,
        file_ids: list[int],
        current_user: User
        ):

        deleted = []
        failed = []

        for file_id in file_ids:

            file = (
                FileRepository.get_user_file_by_id(
                    db,
                    file_id,
                    current_user.id
                )
            )

            if not file:
                failed.append(file_id)
                continue

            FileRepository.soft_delete_file(
                db,
                file
            )

            deleted.append(file_id)

        return {
            "deleted": deleted,
            "failed": failed
        }

    @staticmethod
    def get_deleted_files(
        db: Session,
        current_user: User
        ):

        return FileRepository.get_deleted_files(
            db,
            current_user.id
        )

    @staticmethod
    def restore_file(
        db: Session,
        file_id: int,
        current_user: User
        ):

        file = (
            FileRepository.get_deleted_file_by_id(
                db,
                file_id,
                current_user.id
            )
        )

        if not file:

            raise HTTPException(
                status_code=404,
                detail="Deleted file not found"
            )

        return FileRepository.restore_file(
            db,
            file
        )

    @staticmethod
    def restore_multiple_files(
        db: Session,
        file_ids: list[int],
        current_user: User
        ):

        restored = []
        failed = []

        for file_id in file_ids:

            file = (
                FileRepository.get_deleted_file_by_id(
                    db,
                    file_id,
                    current_user.id
                )
            )

            if not file:
                failed.append(file_id)
                continue

            FileRepository.restore_file(
                db,
                file
            )

            restored.append(file_id)

        return {
            "restored": restored,
            "failed": failed
        }

    @staticmethod
    def permanently_delete_file(
        db: Session,
        file_id: int,
        current_user: User
        ):

        file = (
            FileRepository.get_user_file_by_id(
                db,
                file_id,
                current_user.id
            )
        ) or (
            FileRepository.get_deleted_file_by_id(
                db,
                file_id,
                current_user.id
            )
        )

        if not file:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        return FileRepository.mark_permanent_delete(
            db,
            file
        )

    @staticmethod
    def batch_permanently_delete_files(
        db: Session,
        file_ids: list[int],
        current_user: User
        ):

        deleted = []
        failed = []

        for file_id in file_ids:

            file = (
                FileRepository.get_user_file_by_id(
                    db,
                    file_id,
                    current_user.id
                )
            ) or (
                FileRepository.get_deleted_file_by_id(
                    db,
                    file_id,
                    current_user.id
                )
            )

            if not file:
                failed.append(file_id)
                continue

            FileRepository.mark_permanent_delete(db, file)
            deleted.append(file_id)

        return {
            "deleted": deleted,
            "failed": failed
        }

    @staticmethod
    def cleanup_permanently_deleted_files(
        db: Session,
        current_user: User
        ):

        files = FileRepository.get_permanently_deleted_files(
            db,
            current_user.id
        )

        removed = []
        missing = []

        for file in files:
            if StorageService.provider.file_exists(file.storage_path):
                StorageService.provider.delete_file(file.storage_path)
                removed.append(file.id)
            else:
                missing.append(file.id)

        return {
            "removed": removed,
            "missing": missing
        }
