from pydantic import BaseModel

from typing import Optional


class CreateFolderRequest(BaseModel):

    name: str

    parent_folder_id: Optional[int] = None


class FolderResponse(BaseModel):

    id: int

    name: str

    owner_id: int

    parent_folder_id: Optional[int]

    class Config:

        from_attributes = True