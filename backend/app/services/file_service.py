from fastapi import (
    HTTPException,
    UploadFile
)
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.file_repository import (FileRepository)
from app.repositories.folder_repository import (FolderRepository)
from app.services.storage_service import (StorageService)
from app.storage.utils.file_utils import (calculate_checksum)


class FileService:

    @staticmethod
    def upload_file(
        db: Session,
        file: UploadFile,
        current_user: User,
        folder_id: int | None
        ):

        if folder_id is not None:
            folder = FolderRepository.get_by_id(db,folder_id)

            if not folder:
                raise HTTPException(status_code=404,detail="Folder not found")

            if folder.owner_id != current_user.id:
                raise HTTPException(status_code=403,detail="Access denied")

        temp_filename = (
            StorageService.provider.save_temp_file(
                file.file,
                file.filename
                )
            )
        
        checksum, file_size = calculate_checksum(file.file)

        storage_path = (
            StorageService.provider.move_temp_to_final(
                temp_filename,
                file.filename
            )
        )

        saved_file = (
            FileRepository.create_file(
                db=db,
                original_filename=file.filename,
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

        if not StorageService.provider.file_exists(file.storage_path):
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

        # if StorageService.provider.file_exists(file.storage_path):
        #     StorageService.provider.delete_file(file.storage_path)

        FileRepository.soft_delete_file(db, file)

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