from abc import ABC, abstractmethod
from typing import List, Set

from src.core.entities import ShelfItem, Shelf, CollateResult


class ShelfItemRepositoryInterface(ABC):

    @abstractmethod
    def read_all(self, shelf: Shelf) -> List[ShelfItem]:
        raise NotImplementedError

    @abstractmethod
    def add(self, shelf: Shelf, items: List[ShelfItem]) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self, shelf: Shelf, items: List[ShelfItem]) -> None:
        raise NotImplementedError

    @abstractmethod
    def collate(self, shelf: Shelf, items: Set[ShelfItem]) -> CollateResult:
        raise NotImplementedError
