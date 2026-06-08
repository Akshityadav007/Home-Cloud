from sqlalchemy.orm import Session
from app.models.folder import Folder


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
            Folder.owner_id == owner_id
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
            Folder.parent_folder_id == None
        ).all()


    @staticmethod
    def get_child_folders(db: Session, owner_id: int, parent_folder_id: int):
        return db.query(Folder).filter(
            Folder.owner_id == owner_id,
            Folder.parent_folder_id == parent_folder_id
        ).all()