import logging.config
from typing import Dict, List

from src.config import Config
from src.core.adapters import (payload_to_catalog, payload_to_profile,
                               payload_to_shelf, payload_to_shelves)
from src.core.entities import Book
from src.core.usecases import (RefreshShelfItemsUseCase,
                               RefreshShelvesfUseCase,
                               SearchLatestBooksUseCase)
from src.dataproviders.repositories import DataRepository

config = Config()

logging.config.fileConfig(config)


def search_latest_books(catalog: Dict, included_shelves: List, excluded_shelves: List) -> Dict:
    result: List[Book] = SearchLatestBooksUseCase(DataRepository()).execute(
        catalog=payload_to_catalog(catalog),
        included_shelves=payload_to_shelves(included_shelves),
        excluded_shelves=payload_to_shelves(excluded_shelves),
    )

    return {"items": [book.to_dict() for book in result]}


def refresh_shelves(profile: Dict) -> None:
    RefreshShelvesfUseCase(DataRepository()).execute(payload_to_profile(profile))


def refresh_shelf_items(shelf: Dict) -> None:
    RefreshShelfItemsUseCase(DataRepository()).execute(payload_to_shelf(shelf))
