import asyncio
import rq
import redis
import logging
from typing import Dict, List, Any

from src.config import Config
from src.core.entities import Book, Catalog, Shelf
from src.core.usecases import SearchLatestBooksUseCase
from src.dataproviders.repositories import DataRepository
from src.dataproviders.gateways import DataGateway


config = Config()
logger = logging.getLogger('src.entrypoints.jobs')


def search_latest_books(catalog: dict, included_shelves: list, excluded_shelves: list) -> Dict:
    logger.info(f'Searching latest books in {catalog["name"]}')

    awaitable_response = SearchLatestBooksUseCase(DataRepository()).execute(
        catalog=Catalog(**catalog),
        included_shelves=[Shelf(**shelf) for shelf in included_shelves],
        excluded_shelves=[Shelf(**shelf) for shelf in excluded_shelves],
    )

    result: List[Book] = asyncio.run(awaitable_response)

    logger.info(f'Search found {len(result)} latest books in {catalog["name"]}')

    return {"items": [book.to_dict() for book in result]}


def on_result(job: rq.job.Job, connection: redis.Redis, result: Any) -> None:

    job.meta["progress"] = 100

    job.save()

    client_id: int = job.meta.get("client_id", 0)

    if client_id:
        logger.info(f'Pushing job {job.get_id()} result to client {client_id}.')

        DataGateway().client.push(client_id=client_id, job_id=job.get_id(), operation="job-result")
