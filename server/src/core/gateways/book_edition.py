from abc import abstractmethod
from typing import List

from src.core.entities import ShelfItem
from src.core.entities.book_edition import BookEdition
from src.core.gateways.base import IGateway


class IBookEditionGateway(IGateway):
    @abstractmethod
    async def fetch_for_shelf_item(self, shelf_item: ShelfItem) -> List[BookEdition]:
        ...
