from pydantic import BaseModel
from app.schemas.folder import FolderResponse
from app.schemas.file import FileResponse


class FolderContentsResponse(BaseModel):

    folders: list[FolderResponse]
    files: list[FileResponse]