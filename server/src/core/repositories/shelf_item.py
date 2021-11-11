from abc import abstractmethod
from typing import List

from src.core.entities import ShelfItem, Shelf
from src.core.repositories.base import BaseRepository


class ShelfItemRepositoryInterface(BaseRepository):

    @abstractmethod
    def read_all(self, shelf: Shelf) -> List[ShelfItem]:
        raise NotImplementedError

    @abstractmethod
    def create_all(self, items: List[ShelfItem]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, items: List[ShelfItem]) -> None:
        raise NotImplementedError
