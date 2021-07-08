import asyncio
import itertools
import logging
from typing import List, Optional, Set

from src.core.entities import Book, Catalog, Profile, Shelf
from src.core.repositories import DataRepositoryInterface
from src.core.usecases.refresh_shelf_books import RefreshShelfBooksUseCase

logger = logging.getLogger('src.core.usecases')


class SearchLatestBooksUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository
        self._refresh_shelf_use_case = RefreshShelfBooksUseCase(repository)

    async def execute(
        self,
        catalog: Catalog,
        profile: Profile,
        included_shelves: List[Shelf],
        excluded_shelves: Optional[List[Shelf]] = None,
    ) -> List[Book]:

        awaitables = [self._refresh_shelf_use_case.execute(profile, shelf)
                      for shelf in itertools.chain(included_shelves, (excluded_shelves or []))]

        if awaitables:
            await asyncio.gather(*awaitables)

        latest_books: List[Book] = []

        if not latest_books:
            return []

        included_books: Set[Book] = set()

        excluded_books: Set[Book] = set()

        for shelf in included_shelves:
            books = await self._repository.gateway.shelves.books(shelf)

            included_books.update((book for book in books if book.isbn is not None))

        if excluded_shelves:
            for shelf in excluded_shelves:
                books = await self._repository.gateway.shelves.books(shelf)

                excluded_books.update((book for book in books if book.isbn is not None))

        matching_books = included_books.difference(excluded_books).intersection(latest_books)

        return sorted(matching_books)
