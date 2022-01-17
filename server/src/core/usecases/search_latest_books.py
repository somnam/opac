import logging
from typing import List, Optional, Set

from src.core.entities import Book, Catalog, Shelf
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class SearchLatestBooksUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    def execute(
        self,
        catalog: Catalog,
        included_shelves: List[Shelf],
        excluded_shelves: Optional[List[Shelf]] = None,
    ) -> List[Book]:
        logger.info(f'Searching latest books in {catalog.name}')

        with self._repository.unit_of_work():
            latest_books: List[Book] = list(self._repository.latest_book.search(
                catalog_uuid=catalog.uuid,
            ))

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
            shelf_items = self._repository.shelf_item.search(shelf_uuid=shelf.uuid)

            included_books.update((shelf_item.book for shelf_item in shelf_items
                                   if shelf_item.isbn is not None))

        if excluded_shelves:
            for shelf in excluded_shelves:
                shelf_items = self._repository.shelf_item.search(shelf_uuid=shelf.uuid)

                excluded_books.update((shelf_item.book for shelf_item in shelf_items
                                       if shelf_item.isbn is not None))

        matching_books = included_books.difference(excluded_books).intersection(latest_books)

        if matching_books:
            logger.info(f'Search found {len(matching_books)} latest books in {catalog.name}')

        return sorted(matching_books)
