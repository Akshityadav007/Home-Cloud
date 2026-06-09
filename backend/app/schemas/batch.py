from pydantic import BaseModel

class BatchFileOperationRequest(BaseModel):

    file_ids: list[int]


class BatchDeleteResponse(BaseModel):

    deleted: list[int]
    failed: list[int]


class BatchRestoreResponse(BaseModel):

    restored: list[int]
    failed: list[int]


class BatchPermanentDeleteResponse(BaseModel):

    deleted: list[int]
    failed: list[int]
