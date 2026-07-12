from pydantic import BaseModel, ConfigDict

from typing import Optional


class CreateFolderRequest(BaseModel):

    name: str

    parent_folder_id: Optional[int] = None


class FolderResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str

    owner_id: int

    parent_folder_id: Optional[int]
