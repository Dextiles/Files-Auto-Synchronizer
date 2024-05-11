from abc import ABC, abstractmethod
from typing import NoReturn


class CloudService(ABC):
    @abstractmethod
    def __init__(self, token: str) -> NoReturn:
        self._token = token
        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self._token}'
        }

    @abstractmethod
    def load(self, file_path: str, file_name: str) -> NoReturn:
        pass

    @abstractmethod
    def reload(self, file_path: str, file_name: str) -> NoReturn:
        pass

    @abstractmethod
    def delete(self, file_path: str) -> NoReturn:
        pass

    @abstractmethod
    def get_info(self) -> dict:
        pass
