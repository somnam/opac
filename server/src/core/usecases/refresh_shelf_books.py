from typing import Set

from src.core.entities import Shelf, ShelfItem, CollateResult
from src.core.repositories import DataRepositoryInterface


class RefreshShelfItemsUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    async def execute(self, shelf: Shelf) -> None:

        shelf_items: Set[ShelfItem] = await self._repository.gateway.shelf.items(shelf)

        result: CollateResult = self._repository.shelf.collate(shelf, shelf_items)

        if result.new:
            self._repository.shelf.add_items(shelf, result.new)

        if result.deleted:
            self._repository.shelf.remove_items(shelf, result.deleted)
