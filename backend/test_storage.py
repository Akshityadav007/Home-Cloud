from io import BytesIO

from app.services.storage_service import (
    StorageService
)


fake_file = BytesIO(
    b"hello storage system"
)

path = StorageService.provider.save_file(
    fake_file,
    "test.txt"
)

print(path)