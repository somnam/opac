import logging
from typing import List, Optional, Set

from src.core.entities import Book, Catalog, Shelf
from src.core.repositories import DataRepositoryInterface

logger = logging.getLogger('src.core.usecases')


class SearchLatestBooksUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    async def execute(
        self,
        catalog: Catalog,
        included_shelves: List[Shelf],
        excluded_shelves: Optional[List[Shelf]] = None,
    ) -> List[Book]:

        with self._repository.catalog.unit_of_work():
            latest_books: List[Book] = self._repository.catalog.latest_books(catalog)

        if not latest_books:
            # TMP
            for book in (
                Book(
                    title="Tęcza grawitacji",
                    author="Thomas Pynchon",
                    isbn="8374692952",
                ),
                Book(
                    title="Infinite Jest",
                    author="David Foster Wallace",
                    isbn="0316920045",
                ),
                Book(
                    title="The World Atlas of Coffee",
                    author="James Hoffmann",
                    isbn="9781784724290",
                ),
                Book(
                    title="Zaśpiewam Ci piosenkę",
                    author="Yang Fumin",
                    isbn="9788380029668",
                ),
            ):
                latest_books.append(book)

            return latest_books

        included_books: Set[Book] = set()

        excluded_books: Set[Book] = set()

        for shelf in included_shelves:
            shelf_items = await self._repository.shelf_item.read_all(shelf)

            included_books.update((shelf_item.book for shelf_item in shelf_items
                                   if shelf_item.book.isbn is not None))

        if excluded_shelves:
            for shelf in excluded_shelves:
                shelf_items = await self._repository.shelf_item.read_all(shelf)

                excluded_books.update((shelf_item.book for shelf_item in shelf_items
                                       if shelf_item.book.isbn is not None))

        matching_books = included_books.difference(excluded_books).intersection(latest_books)

        return sorted(matching_books)
