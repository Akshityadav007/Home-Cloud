from sqlalchemy.orm import Session

from app.models.user import User
from app.services.advanced_service import AdvancedService
from app.services.file_service import FileService


def run_user_storage_maintenance(db: Session, user: User):
    permanent_delete_cleanup = FileService.cleanup_permanently_deleted_files(
        db,
        user
    )
    consistency_report = AdvancedService.consistency_report(
        db,
        user
    )
    upload_session_cleanup = AdvancedService.cleanup_expired_upload_sessions(
        db,
        user
    )

    return {
        "permanent_delete_cleanup": permanent_delete_cleanup,
        "consistency_report": consistency_report,
        "upload_session_cleanup": upload_session_cleanup
    }
