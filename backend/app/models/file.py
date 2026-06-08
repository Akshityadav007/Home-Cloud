from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    BigInteger,
    DateTime
)

from sqlalchemy.sql import func

from app.core.database import Base


class File(Base):

    __tablename__ = "files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    original_filename = Column(
        String,
        nullable=False
    )

    storage_path = Column(
        String,
        nullable=False,
        unique=True
    )

    mime_type = Column(
        String,
        nullable=True
    )

    size_bytes = Column(
        BigInteger,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    folder_id = Column(
        Integer,
        ForeignKey("folders.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )