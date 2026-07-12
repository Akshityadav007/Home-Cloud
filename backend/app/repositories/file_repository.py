from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.file import File
from datetime import datetime, timezone

class FileRepository:

    @staticmethod
    def create_file(
        db: Session,
        original_filename: str,
        storage_path: str,
        mime_type: str | None,
        size_bytes: int,
        owner_id: int,
        folder_id: int | None,
        checksum: str
        ):

        file = File(
            original_filename=original_filename,
            storage_path=storage_path,
            mime_type=mime_type,
            size_bytes=size_bytes,
            owner_id=owner_id,
            folder_id=folder_id,
            checksum=checksum
        )

        db.add(file)
        db.commit()
        db.refresh(file)

        return file

    @staticmethod
    def get_user_files(db: Session, owner_id: int):
        return db.query(File).filter(
            File.owner_id == owner_id,
            File.deleted_at.is_(None)
            ).all()

    @staticmethod
    def get_by_id(
        db: Session,
        file_id: int
        ):

        return db.query(File).filter(
            File.id == file_id,
            File.deleted_at.is_(None)
        ).first()

    @staticmethod
    def get_user_file_by_id(
        db: Session,
        file_id: int,
        owner_id: int
        ):
        return db.query(File).filter(
            File.id == file_id,
            File.owner_id == owner_id,
            File.deleted_at.is_(None)
        ).first()

    @staticmethod
    def get_user_files_by_ids(
        db: Session,
        file_ids: list[int],
        owner_id: int
        ):

        return db.query(File).filter(
            File.id.in_(file_ids),
            File.owner_id == owner_id,
            File.deleted_at.is_(None)
        ).all()

    @staticmethod
    def get_used_storage_bytes(
        db: Session,
        owner_id: int
        ):

        return db.query(
            func.coalesce(func.sum(File.size_bytes), 0)
        ).filter(
            File.owner_id == owner_id,
            File.is_permanent_delete == False
        ).scalar()

    @staticmethod
    def soft_delete_file(
        db: Session,
        file: File
        ):

        file.deleted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(file)

    @staticmethod
    def get_root_files(
        db: Session,
        owner_id: int
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.folder_id.is_(None),
            File.deleted_at.is_(None)
        ).all()

    @staticmethod
    def get_folder_files(
        db: Session,
        owner_id: int,
        folder_id: int
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.folder_id == folder_id,
            File.deleted_at.is_(None)
        ).all()

    @staticmethod
    def get_folder_files_for_lifecycle(
        db: Session,
        owner_id: int,
        folder_id: int
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.folder_id == folder_id,
            File.is_permanent_delete == False
        ).all()

    @staticmethod
    def search_files(
        db: Session,
        owner_id: int,
        query: str
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.deleted_at.is_(None),
            File.original_filename.ilike(f"%{query}%")
        ).all()

    @staticmethod
    def get_deleted_files(
        db: Session,
        owner_id: int
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.deleted_at.is_not(None),
            File.is_permanent_delete == False
        ).all()

    @staticmethod
    def get_deleted_file_by_id(
        db: Session,
        file_id: int,
        owner_id: int
        ):

        return db.query(File).filter(
            File.id == file_id,
            File.owner_id == owner_id,
            File.deleted_at.is_not(None),
            File.is_permanent_delete == False
        ).first()

    @staticmethod
    def restore_file(
        db: Session,
        file: File
        ):

        file.deleted_at = None
        file.is_permanent_delete = False
        db.commit()
        db.refresh(file)

        return file

    @staticmethod
    def mark_permanent_delete(
        db: Session,
        file: File
        ):

        file.deleted_at = datetime.now(timezone.utc)
        file.is_permanent_delete = True
        db.commit()
        db.refresh(file)

        return file

    @staticmethod
    def get_permanently_deleted_files(
        db: Session,
        owner_id: int
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.is_permanent_delete == True
        ).all()

    @staticmethod
    def get_all_non_permanent_user_files(
        db: Session,
        owner_id: int
        ):

        return db.query(File).filter(
            File.owner_id == owner_id,
            File.is_permanent_delete == False
        ).all()
