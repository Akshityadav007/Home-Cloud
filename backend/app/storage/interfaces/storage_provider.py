from abc import ABC, abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    def save_file(
        self,
        file_data,
        filename: str
    ) -> str:
        pass


    @abstractmethod
    def get_file_path(
        self,
        filename: str
    ) -> str:
        pass


    @abstractmethod
    def delete_file(
        self,
        filename: str
    ):
        pass


    @abstractmethod
    def file_exists(
        self,
        filename: str
    ) -> bool:
        pass