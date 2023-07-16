from abc import abstractmethod
from typing import Sequence

from src.core.entities.book_edition import BookEdition
from src.core.entities.shelf import Shelf
from src.core.repositories.entity import IEntityRepository


class IBookEditionRepository(IEntityRepository[BookEdition]):
    @abstractmethod
    async def sync_on_shelf(self, shelf: Shelf, book_editions: Sequence[BookEdition]) -> None:
        ...
