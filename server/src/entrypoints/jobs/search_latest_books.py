import asyncio
import logging
from typing import List, Optional

from src.config import Config
from src.core.entities import Book, Catalog, Profile, Shelf
from src.core.usecases import SearchLatestBooksUseCase
from src.dataproviders.repositories import DataRepository

config = Config()
logger = logging.getLogger('src.entrypoints.jobs')


def search_latest_books(catalog: dict, profile: dict) -> Optional[List[dict]]:
    logger.warn(f'Searching latest books for {profile["name"]} in {catalog["name"]}')

    use_case = SearchLatestBooksUseCase(repository=DataRepository())

    awaitable_response = use_case.execute(
        catalog=Catalog(**catalog),
        profile=Profile(**profile),
        included_shelves=[Shelf(**shelf) for shelf in
                          config.getstruct('latest_books_scraper', 'included_shelves')],
        excluded_shelves=[Shelf(**shelf) for shelf in
                          config.getstruct('latest_books_scraper', 'excluded_shelves')],
    )

    result: List[Book] = asyncio.run(awaitable_response)

    logger.warn(f'Search found {len(result)} latest books for {profile["name"]} in {catalog["name"]}')

    return {
        "catalog": catalog,
        "profile": profile,
        "items": [book.to_dict() for book in result],
    }
