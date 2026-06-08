from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileResponse(BaseModel):

    id: int
    original_filename: str
    mime_type: Optional[str]
    size_bytes: int
    owner_id: int
    folder_id: Optional[int]
    created_at: datetime
    checksum: str

    class Config:
        
        from_attributes = True