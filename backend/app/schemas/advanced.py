from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateShareRequest(BaseModel):

    shared_with_user_id: Optional[int] = None
    permission: str = "read"
    expires_at: Optional[datetime] = None


class ShareResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: int
    owner_id: int
    shared_with_user_id: Optional[int]
    token: str
    permission: str
    expires_at: Optional[datetime]
    revoked_at: Optional[datetime]


class CreateUploadSessionRequest(BaseModel):

    original_filename: str
    total_size: int
    chunk_size: int
    mime_type: Optional[str] = None
    folder_id: Optional[int] = None


class UploadSessionResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    total_size: int
    chunk_size: int
    total_chunks: int
    received_chunks_json: str
    completed_at: Optional[datetime]
    expires_at: datetime


class FileVersionResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: int
    version_number: int
    size_bytes: int
    checksum: str
    created_at: datetime


class DeviceRequest(BaseModel):

    client_id: str
    name: str


class DeviceResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: str
    name: str
    created_at: datetime
    last_seen_at: datetime


class ConflictRequest(BaseModel):

    file_id: int
    client_checksum: str


class StorageVolumeRequest(BaseModel):

    name: str
    path: str


class AuditLogResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int]
    action: str
    resource_type: str
    resource_id: Optional[int]
    metadata_json: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
