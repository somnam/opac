from abc import ABC, abstractmethod
from typing import List, Set

from src.core.entities import ShelfItem, Shelf, CollateResult


class ShelfRepositoryInterface(ABC):

    @abstractmethod
    def items(self, shelf: Shelf) -> List[ShelfItem]:
        raise NotImplementedError

    @abstractmethod
    def add_items(self, shelf: Shelf, items: List[ShelfItem]) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_items(self, shelf: Shelf, items: List[ShelfItem]) -> None:
        raise NotImplementedError

    @abstractmethod
    def collate(self, shelf: Shelf, items: Set[ShelfItem]) -> CollateResult:
        raise NotImplementedError
