from typing import List, Set

from src.core.entities import Shelf, ShelfItem, CollateResult
from src.core.repositories import ShelfItemRepositoryInterface
from src.dataproviders.mixin import DbHandlerMixin


class ShelItemfRepository(ShelfItemRepositoryInterface, DbHandlerMixin):

    def read_all(self, shelf: Shelf) -> List[ShelfItem]:
        return []

    def add(self, shelf: Shelf, items: List[ShelfItem]) -> None:
        if not items:
            return

    def remove(self, shelf: Shelf, items: List[ShelfItem]) -> None:
        if not items:
            return

    def collate(self, shelf: Shelf, items: Set[ShelfItem]) -> CollateResult:
        existing_items = set(self.read_all(shelf))

        new_items = items.difference(existing_items)

        deleted_items = existing_items.difference(items)

        return CollateResult(
            new=new_items,
            deleted=deleted_items,
        )
