import json
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.audit_log import AuditLog
from app.models.device import Device
from app.models.file_version import FileVersion
from app.models.share import Share
from app.models.storage_volume import StorageVolume
from app.models.sync_event import SyncEvent
from app.models.upload_session import UploadSession


class AuditRepository:

    @staticmethod
    def create_log(
        db: Session,
        user_id: int | None,
        action: str,
        resource_type: str,
        resource_id: int | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None
        ):

        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata_json=json.dumps(metadata or {}),
            ip_address=ip_address
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def list_user_logs(db: Session, user_id: int):
        return db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(AuditLog.id.desc()).all()


class VersionRepository:

    @staticmethod
    def create_version(
        db: Session,
        file_id: int,
        storage_path: str,
        size_bytes: int,
        checksum: str
        ):

        latest = db.query(FileVersion).filter(
            FileVersion.file_id == file_id
        ).order_by(FileVersion.version_number.desc()).first()

        version = FileVersion(
            file_id=file_id,
            version_number=(latest.version_number + 1 if latest else 1),
            storage_path=storage_path,
            size_bytes=size_bytes,
            checksum=checksum
        )
        db.add(version)
        db.commit()
        db.refresh(version)
        return version

    @staticmethod
    def list_versions(db: Session, file_id: int):
        return db.query(FileVersion).filter(
            FileVersion.file_id == file_id
        ).order_by(FileVersion.version_number.desc()).all()

    @staticmethod
    def get_version(db: Session, file_id: int, version_number: int):
        return db.query(FileVersion).filter(
            FileVersion.file_id == file_id,
            FileVersion.version_number == version_number
        ).first()


class ShareRepository:

    @staticmethod
    def create_share(
        db: Session,
        file_id: int,
        owner_id: int,
        shared_with_user_id: int | None,
        permission: str,
        expires_at: datetime | None
        ):

        share = Share(
            file_id=file_id,
            owner_id=owner_id,
            shared_with_user_id=shared_with_user_id,
            token=secrets.token_urlsafe(32),
            permission=permission,
            expires_at=expires_at
        )
        db.add(share)
        db.commit()
        db.refresh(share)
        return share

    @staticmethod
    def get_active_by_token(db: Session, token: str):
        now = datetime.now(timezone.utc)
        share = db.query(Share).filter(
            Share.token == token,
            Share.revoked_at.is_(None)
        ).first()

        if share and share.expires_at:
            comparable_now = now

            if share.expires_at.tzinfo is None:
                comparable_now = now.replace(tzinfo=None)

            if share.expires_at < comparable_now:
                return None

        return share

    @staticmethod
    def list_user_shares(db: Session, owner_id: int):
        return db.query(Share).filter(
            Share.owner_id == owner_id,
            Share.revoked_at.is_(None)
        ).all()

    @staticmethod
    def revoke_share(db: Session, share: Share):
        share.revoked_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(share)
        return share


class UploadSessionRepository:

    @staticmethod
    def create_session(
        db: Session,
        owner_id: int,
        folder_id: int | None,
        original_filename: str,
        mime_type: str | None,
        total_size: int,
        chunk_size: int,
        total_chunks: int
        ):

        session = UploadSession(
            owner_id=owner_id,
            folder_id=folder_id,
            original_filename=original_filename,
            mime_type=mime_type,
            total_size=total_size,
            chunk_size=chunk_size,
            total_chunks=total_chunks,
            received_chunks_json="[]",
            expires_at=datetime.now(timezone.utc) + timedelta(
                hours=settings.UPLOAD_SESSION_TTL_HOURS
            )
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_user_session(db: Session, session_id: int, owner_id: int):
        return db.query(UploadSession).filter(
            UploadSession.id == session_id,
            UploadSession.owner_id == owner_id
        ).first()

    @staticmethod
    def mark_chunk_received(
        db: Session,
        session: UploadSession,
        chunk_index: int
        ):

        chunks = set(json.loads(session.received_chunks_json))
        chunks.add(chunk_index)
        session.received_chunks_json = json.dumps(sorted(chunks))
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def complete_session(db: Session, session: UploadSession):
        session.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(session)
        return session


class DeviceRepository:

    @staticmethod
    def upsert_device(
        db: Session,
        owner_id: int,
        client_id: str,
        name: str
        ):

        device = db.query(Device).filter(
            Device.client_id == client_id,
            Device.owner_id == owner_id
        ).first()

        if device:
            device.name = name
            device.last_seen_at = datetime.now(timezone.utc)
        else:
            device = Device(
                owner_id=owner_id,
                client_id=client_id,
                name=name
            )
            db.add(device)

        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def list_devices(db: Session, owner_id: int):
        return db.query(Device).filter(
            Device.owner_id == owner_id
        ).all()


class SyncRepository:

    @staticmethod
    def create_event(
        db: Session,
        owner_id: int,
        event_type: str,
        resource_type: str,
        resource_id: int | None
        ):

        event = SyncEvent(
            owner_id=owner_id,
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def list_events_after(db: Session, owner_id: int, after_id: int):
        return db.query(SyncEvent).filter(
            SyncEvent.owner_id == owner_id,
            SyncEvent.id > after_id
        ).order_by(SyncEvent.id.asc()).all()


class StorageVolumeRepository:

    @staticmethod
    def create_volume(db: Session, name: str, path: str):
        volume = StorageVolume(name=name, path=path)
        db.add(volume)
        db.commit()
        db.refresh(volume)
        return volume

    @staticmethod
    def list_volumes(db: Session):
        return db.query(StorageVolume).all()
