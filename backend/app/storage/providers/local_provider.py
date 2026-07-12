import os
import shutil
import uuid

from pathlib import Path
from app.core.config import settings

from app.storage.interfaces.storage_provider import (
    StorageProvider
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

def _resolve_storage_path(path_value: str) -> Path:
    path = Path(path_value)

    if not path.is_absolute():
        path = BASE_DIR / path

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


BASE_STORAGE_PATH = _resolve_storage_path(settings.STORAGE_ROOT_PATH)
TEMP_STORAGE_PATH = _resolve_storage_path(settings.TEMP_STORAGE_PATH)

class LocalStorageProvider(StorageProvider):

    def save_file( self, file_data, filename: str) -> str:
        extension = Path(filename).suffix
        generated_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        first_level = generated_filename[:2]
        second_level = generated_filename[2:4]

        target_directory = (
            BASE_STORAGE_PATH /
            first_level /
            second_level
        )

        os.makedirs(
            target_directory,
            exist_ok=True
        )

        target_path = (target_directory / generated_filename)

        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(
                file_data,
                buffer
            )

        relative_path = (
            f"{first_level}/"
            f"{second_level}/"
            f"{generated_filename}"
        )

        return relative_path

    def get_file_path( self, filename: str) -> str:
        return str(BASE_STORAGE_PATH / filename)

    def delete_file( self, filename: str):
        path = BASE_STORAGE_PATH / filename
        if path.exists():
            os.remove(path)

    def file_exists( self, filename: str) -> bool:
        return (BASE_STORAGE_PATH / filename).exists()
    
    def open_file( self, filename: str):
        path = BASE_STORAGE_PATH / filename
        return open(path, "rb")

    def save_temp_file(self, file_data, filename: str):
        extension = Path(filename).suffix
        temp_filename = (f"{uuid.uuid4()}{extension}")
        temp_path = (TEMP_STORAGE_PATH / temp_filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file_data, buffer)

        return temp_filename

    def move_temp_to_final(self, temp_filename: str, original_filename: str):

        extension = Path(original_filename).suffix

        generated_filename = (f"{uuid.uuid4()}{extension}")

        first_level = generated_filename[:2]
        second_level = generated_filename[2:4]

        target_directory = (
            BASE_STORAGE_PATH /
            first_level /
            second_level
        )

        os.makedirs(target_directory, exist_ok=True)

        temp_path = (TEMP_STORAGE_PATH / temp_filename)

        final_path = (
            target_directory /
            generated_filename
        )

        shutil.move(
            temp_path,
            final_path
        )

        return (
            f"{first_level}/"
            f"{second_level}/"
            f"{generated_filename}"
        )

    def temp_file_exists(self, filename: str) -> bool:
        return (TEMP_STORAGE_PATH / filename).exists()

    def delete_temp_file(self, filename: str):
        path = TEMP_STORAGE_PATH / filename
        if path.exists():
            os.remove(path)

    def list_storage_files(self) -> list[str]:
        files = []

        for path in BASE_STORAGE_PATH.rglob("*"):
            if path.is_file():
                files.append(path.relative_to(BASE_STORAGE_PATH).as_posix())

        return files
