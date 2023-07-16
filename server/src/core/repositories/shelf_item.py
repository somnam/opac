from abc import abstractmethod
from typing import List, Sequence

from src.core.entities import Shelf, ShelfItem
from src.core.repositories.entity import IEntityRepository


class IShelfItemRepository(IEntityRepository[ShelfItem]):
    @abstractmethod
    async def read_all_on_shelf(self, shelf: Shelf) -> List[ShelfItem]:
        ...

    @abstractmethod
    async def sync_on_shelf(self, shelf: Shelf, shelf_items: Sequence[ShelfItem]) -> None:
        ...
