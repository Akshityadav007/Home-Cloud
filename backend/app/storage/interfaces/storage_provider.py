from abc import ABC, abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    def save_file( self, file_data, filename: str) -> str:
        pass

    @abstractmethod
    def get_file_path( self, filename: str) -> str:
        pass


    @abstractmethod
    def delete_file( self, filename: str):
        pass


    @abstractmethod
    def file_exists( self, filename: str) -> bool:
        pass

    @abstractmethod
    def open_file( self, filename: str):
        pass

    @abstractmethod
    def save_temp_file(self, file_data, filename: str):
        pass

    @abstractmethod
    def move_temp_to_final(self, temp_filename: str, original_filename: str):
        pass

    @abstractmethod
    def temp_file_exists(self, filename: str) -> bool:
        pass

    @abstractmethod
    def delete_temp_file(self, filename: str):
        pass

    @abstractmethod
    def list_storage_files(self) -> list[str]:
        pass

    @abstractmethod
    def get_temp_file_path(self, filename: str) -> str:
        pass

    @abstractmethod
    def open_temp_file(self, filename: str):
        pass

    @abstractmethod
    def save_upload_chunk(self, session_id: int, chunk_index: int, file_data):
        pass

    @abstractmethod
    def assemble_upload_chunks(self, session_id: int, total_chunks: int) -> str:
        pass

    @abstractmethod
    def save_thumbnail(self, file_storage_path: str, thumbnail_data):
        pass

    @abstractmethod
    def list_temp_files(self) -> list[str]:
        pass
