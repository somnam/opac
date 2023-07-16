import logging
from typing import List, Optional

from src.core.entities import Catalog, LatestBook, Shelf
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class SearchLatestBooksUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        catalog: Catalog,
        included_shelves: List[Shelf],
        excluded_shelves: Optional[List[Shelf]] = None,
    ) -> List[LatestBook]:
        logger.info(f"Searching latest books in {catalog.name}")

        async with self._repository.context():
            latest_books = await self._repository.latest_book.search_in_catalog_by_shelves(
                catalog=catalog,
                included_shelves=included_shelves,
                excluded_shelves=excluded_shelves,
            )

        if not latest_books:
            logger.info(f"Search did not find matching books in {catalog.name}")
            return []

        return sorted(latest_books)
