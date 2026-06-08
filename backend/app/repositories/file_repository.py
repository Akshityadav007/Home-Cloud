from sqlalchemy.orm import Session
from app.models.file import File


class FileRepository:

    @staticmethod
    def create_file(
        db: Session,
        original_filename: str,
        storage_path: str,
        mime_type: str | None,
        size_bytes: int,
        owner_id: int,
        folder_id: int | None
    ):
        file = File(
            original_filename=original_filename,
            storage_path=storage_path,
            mime_type=mime_type,
            size_bytes=size_bytes,
            owner_id=owner_id,
            folder_id=folder_id
        )

        db.add(file)
        db.commit()
        db.refresh(file)

        return file

    @staticmethod
    def get_user_files(db: Session, owner_id: int):
        return db.query(File).filter(
            File.owner_id == owner_id
        ).all()

    @staticmethod
    def get_by_id(db: Session, file_id: int):
        return db.query(File).filter(
            File.id == file_id
        ).first()
    
    @staticmethod
    def get_user_file_by_id(db: Session, file_id: int, owner_id: int):
        return db.query(File).filter(
            File.id == file_id,
            File.owner_id == owner_id
        ).first()

    @staticmethod
    def delete_file(db: Session, file: File):
        db.delete(file)
        db.commit()

    @staticmethod
    def get_root_files(db: Session, owner_id: int):
        return db.query(File).filter(
            File.owner_id == owner_id,
            File.folder_id == None
        ).all()

    @staticmethod
    def get_folder_files(
        db: Session,
        owner_id: int,
        folder_id: int
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.folder_id == folder_id
        ).all()