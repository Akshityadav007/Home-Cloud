from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class FileVersion(Base):

    __tablename__ = "file_versions"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    storage_path = Column(String, nullable=False, unique=True)
    size_bytes = Column(BigInteger, nullable=False)
    checksum = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
