from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.folder_repository import (
    FolderRepository
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
    def get_user_folders(
        db: Session,
        current_user: User
    ):

        return FolderRepository.get_user_folders(
            db,
            current_user.id
        )