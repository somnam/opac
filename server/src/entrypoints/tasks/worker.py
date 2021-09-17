import logging
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
from src.entrypoints.tasks.base import Worker


config = Config()

logging.config.fileConfig(config)

logger = logging.getLogger(__name__)


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


def run() -> None:
    try:
        logger.info("Starting worker.")
        Worker.run()
    except KeyboardInterrupt:
        logger.info("Shutting down worker.")
