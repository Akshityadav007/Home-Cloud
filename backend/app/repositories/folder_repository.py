from sqlalchemy.orm import Session
from app.models.folder import Folder
from datetime import datetime, timezone


class FolderRepository:

    @staticmethod
    def create_folder(
        db: Session,
        name: str,
        owner_id: int,
        parent_folder_id: int | None
        ):

        folder = Folder(
            name=name,
            owner_id=owner_id,
            parent_folder_id=parent_folder_id
        )

        db.add(folder)
        db.commit()
        db.refresh(folder)

        return folder


    @staticmethod
    def get_user_folders(db: Session, owner_id: int):
        return db.query(Folder).filter(
            Folder.owner_id == owner_id,
            Folder.deleted_at.is_(None)
        ).all()


    @staticmethod
    def get_by_id(db: Session, folder_id: int):
        return db.query(Folder).filter(
            Folder.id == folder_id
        ).first()

    @staticmethod
    def get_root_folders(db: Session, owner_id: int):
        return db.query(Folder).filter(
            Folder.owner_id == owner_id,
            Folder.parent_folder_id == None,
            Folder.deleted_at.is_(None)
        ).all()


    @staticmethod
    def get_child_folders(db: Session, owner_id: int, parent_folder_id: int):
        return db.query(Folder).filter(
            Folder.owner_id == owner_id,
            Folder.parent_folder_id == parent_folder_id,
            Folder.deleted_at.is_(None)
        ).all()

    @staticmethod
    def get_active_user_folder_by_id(
        db: Session,
        folder_id: int,
        owner_id: int
        ):

        return db.query(Folder).filter(
            Folder.id == folder_id,
            Folder.owner_id == owner_id,
            Folder.deleted_at.is_(None)
        ).first()

    @staticmethod
    def get_deleted_user_folder_by_id(
        db: Session,
        folder_id: int,
        owner_id: int
        ):

        return db.query(Folder).filter(
            Folder.id == folder_id,
            Folder.owner_id == owner_id,
            Folder.deleted_at.is_not(None),
            Folder.is_permanent_delete == False
        ).first()

    @staticmethod
    def get_child_folders_for_lifecycle(
        db: Session,
        owner_id: int,
        parent_folder_id: int
        ):

        return db.query(Folder).filter(
            Folder.owner_id == owner_id,
            Folder.parent_folder_id == parent_folder_id,
            Folder.is_permanent_delete == False
        ).all()

    @staticmethod
    def get_deleted_folders(db: Session, owner_id: int):

        return db.query(Folder).filter(
            Folder.owner_id == owner_id,
            Folder.deleted_at.is_not(None),
            Folder.is_permanent_delete == False
        ).all()

    @staticmethod
    def soft_delete_folder(
        db: Session,
        folder: Folder
        ):

        folder.deleted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(folder)

        return folder

    @staticmethod
    def restore_folder(
        db: Session,
        folder: Folder
        ):

        folder.deleted_at = None
        folder.is_permanent_delete = False
        db.commit()
        db.refresh(folder)

        return folder

    @staticmethod
    def mark_permanent_delete(
        db: Session,
        folder: Folder
        ):

        folder.deleted_at = datetime.now(timezone.utc)
        folder.is_permanent_delete = True
        db.commit()
        db.refresh(folder)

        return folder
