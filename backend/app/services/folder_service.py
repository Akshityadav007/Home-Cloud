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

        if parent_folder_id is not None:
            parent_folder = FolderRepository.get_active_user_folder_by_id(
                db,
                parent_folder_id,
                current_user.id
            )

            if not parent_folder:
                raise HTTPException(
                    status_code=404,
                    detail="Parent folder not found"
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

        if folder.deleted_at or folder.is_permanent_delete:
            raise HTTPException(
                status_code=404,
                detail="Folder not found"
            )

        folders = (FolderRepository.get_child_folders(db,current_user.id, folder_id))

        files = (FileRepository.get_folder_files(db,current_user.id, folder_id))

        return {
            "folders": folders,
            "files": files
        }

    @staticmethod
    def _collect_folder_subtree(
        db: Session,
        owner_id: int,
        root_folder
        ):

        folders = []
        stack = [root_folder]

        while stack:
            folder = stack.pop()
            folders.append(folder)

            children = FolderRepository.get_child_folders_for_lifecycle(
                db,
                owner_id,
                folder.id
            )

            stack.extend(children)

        return folders

    @staticmethod
    def _folder_subtree_files(
        db: Session,
        owner_id: int,
        folders
        ):

        files = []

        for folder in folders:
            files.extend(
                FileRepository.get_folder_files_for_lifecycle(
                    db,
                    owner_id,
                    folder.id
                )
            )

        return files

    @staticmethod
    def delete_folder(
        db: Session,
        folder_id: int,
        current_user: User
        ):

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

        folders = FolderService._collect_folder_subtree(
            db,
            current_user.id,
            folder
        )

        files = FolderService._folder_subtree_files(
            db,
            current_user.id,
            folders
        )

        for file in files:
            FileRepository.soft_delete_file(db, file)

        for child_folder in folders:
            FolderRepository.soft_delete_folder(db, child_folder)

        return {
            "message": "Folder deleted successfully",
            "folders_deleted": len(folders),
            "files_deleted": len(files)
        }

    @staticmethod
    def get_deleted_folders(
        db: Session,
        current_user: User
        ):

        return FolderRepository.get_deleted_folders(
            db,
            current_user.id
        )

    @staticmethod
    def restore_folder(
        db: Session,
        folder_id: int,
        current_user: User
        ):

        folder = FolderRepository.get_deleted_user_folder_by_id(
            db,
            folder_id,
            current_user.id
        )

        if not folder:
            raise HTTPException(
                status_code=404,
                detail="Deleted folder not found"
            )

        folders = FolderService._collect_folder_subtree(
            db,
            current_user.id,
            folder
        )

        files = FolderService._folder_subtree_files(
            db,
            current_user.id,
            folders
        )

        for file in files:
            FileRepository.restore_file(db, file)

        for child_folder in folders:
            FolderRepository.restore_folder(db, child_folder)

        return folder

    @staticmethod
    def permanently_delete_folder(
        db: Session,
        folder_id: int,
        current_user: User
        ):

        folder = (
            FolderRepository.get_active_user_folder_by_id(
                db,
                folder_id,
                current_user.id
            )
        ) or (
            FolderRepository.get_deleted_user_folder_by_id(
                db,
                folder_id,
                current_user.id
            )
        )

        if not folder:
            raise HTTPException(
                status_code=404,
                detail="Folder not found"
            )

        folders = FolderService._collect_folder_subtree(
            db,
            current_user.id,
            folder
        )

        files = FolderService._folder_subtree_files(
            db,
            current_user.id,
            folders
        )

        for file in files:
            FileRepository.mark_permanent_delete(db, file)

        for child_folder in folders:
            FolderRepository.mark_permanent_delete(db, child_folder)

        return folder
