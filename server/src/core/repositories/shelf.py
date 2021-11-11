from abc import abstractmethod
from typing import List

from src.core.entities import Profile, Shelf
from src.core.repositories.base import BaseRepository


class ShelfRepositoryInterface(BaseRepository):
    @abstractmethod
    def exists(self, shelf_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def read_all(self, profile: Profile) -> List[Shelf]:
        raise NotImplementedError

    @abstractmethod
    def create_all(self, shelves: List[Shelf]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_all(self, shelves: List[Shelf]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, shelves: List[Shelf]) -> None:
        raise NotImplementedError
