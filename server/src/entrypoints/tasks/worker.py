import asyncio
import logging
import logging.config
from typing import Dict

from src.config import Config
from src.core.transforms import payload_to_profile, payload_to_shelf
from src.core.usecases import RefreshShelfItemsUseCase, RefreshShelvesUseCase
from src.dataproviders.gateways import DataGateway
from src.dataproviders.repositories import DataRepository
from src.entrypoints.tasks.base import Worker

config = Config()

logging.config.fileConfig(config)

logger = logging.getLogger(__name__)


def refresh_shelves(profile: Dict) -> None:
    asyncio.get_event_loop().run_until_complete(
        RefreshShelvesUseCase(
            gateway=DataGateway(),
            repository=DataRepository(),
        ).execute(payload_to_profile(profile))
    )


def refresh_shelf_items(shelf: Dict) -> None:
    asyncio.get_event_loop().run_until_complete(
        RefreshShelfItemsUseCase(gateway=DataGateway(), repository=DataRepository()).execute(
            shelf=payload_to_shelf(shelf),
        )
    )


def run() -> None:
    try:
        logger.info("Starting worker.")
        Worker.run()
    except KeyboardInterrupt:
        logger.info("Shutting down worker.")
