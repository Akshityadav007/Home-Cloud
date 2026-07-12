from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class FileResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    mime_type: Optional[str]
    size_bytes: int
    owner_id: int
    folder_id: Optional[int]
    created_at: datetime
    checksum: str
