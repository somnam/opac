from abc import abstractmethod
from typing import List, Optional

from src.core.entities import Catalog, LatestBook, Shelf
from src.core.repositories.entity import IEntityRepository


class ILatestBookRepository(IEntityRepository[LatestBook]):
    @abstractmethod
    async def search_in_catalog_by_shelves(
        self,
        catalog: Catalog,
        included_shelves: List[Shelf],
        excluded_shelves: Optional[List[Shelf]],
    ) -> List[LatestBook]:
        ...
