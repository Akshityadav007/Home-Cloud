from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class UploadSession(Base):

    __tablename__ = "upload_sessions"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    original_filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=True)
    total_size = Column(BigInteger, nullable=False)
    chunk_size = Column(BigInteger, nullable=False)
    total_chunks = Column(Integer, nullable=False)
    received_chunks_json = Column(Text, nullable=False, default="[]")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
