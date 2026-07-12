from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Folder(Base):

    __tablename__ = "folders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    parent_folder_id = Column(
        Integer,
        ForeignKey("folders.id"),
        nullable=True
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    is_permanent_delete = Column(
        Boolean,
        default=False,
        nullable=False
    )

    parent = relationship(
        "Folder",
        remote_side=[id]
    )
