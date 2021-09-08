from abc import ABC, abstractmethod
from typing import List

from src.core.entities import ShelfItem, Shelf


class ShelfItemRepositoryInterface(ABC):

    @abstractmethod
    def read_all(self, shelf: Shelf) -> List[ShelfItem]:
        raise NotImplementedError

    @abstractmethod
    def create_all(self, items: List[ShelfItem]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, items: List[ShelfItem]) -> None:
        raise NotImplementedError
