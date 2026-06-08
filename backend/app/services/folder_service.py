from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.folder_repository import (
    FolderRepository
)
from app.repositories.file_repository import (
    FileRepository
)


class FolderService:

    @staticmethod
    def create_folder(
        db: Session,
        name: str,
        current_user: User,
        parent_folder_id: int | None
        ):

        if parent_folder_id:
            parent_folder = FolderRepository.get_by_id(
                db,
                parent_folder_id
            )

            if not parent_folder:
                raise HTTPException(
                    status_code=404,
                    detail="Parent folder not found"
                )

            if parent_folder.owner_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Access denied"
                )

        return FolderRepository.create_folder(
            db=db,
            name=name,
            owner_id=current_user.id,
            parent_folder_id=parent_folder_id
        )


    @staticmethod
    def get_user_folders(db: Session, current_user: User):
        return FolderRepository.get_user_folders(db, current_user.id)
    
    @staticmethod
    def get_root_contents(
        db: Session,
        current_user: User
        ):

        folders = (
            FolderRepository.get_root_folders(
                db,
                current_user.id
            )
        )

        files = (
            FileRepository.get_root_files(
                db,
                current_user.id
            )
        )

        return {
            "folders": folders,
            "files": files
        }


    @staticmethod
    def get_folder_contents(db: Session,current_user: User, folder_id: int):

        folder = FolderRepository.get_by_id(db, folder_id)

        if not folder:
            raise HTTPException(
                status_code=404,
                detail="Folder not found"
            )

        if folder.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        folders = (FolderRepository.get_child_folders(db,current_user.id, folder_id))

        files = (FileRepository.get_folder_files(db,current_user.id, folder_id))

        return {
            "folders": folders,
            "files": files
        }