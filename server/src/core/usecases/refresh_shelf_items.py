import asyncio
import logging
from datetime import datetime
from typing import List

from src.core.entities import Collate, ScheduleItem, Shelf
from src.core.exceptions import ProfileNotFoundError
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class RefreshShelfItemsUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    def execute(self, shelf: Shelf) -> None:
        logger.info(f'Refreshing items on shelf {shelf.name}')

        with self._repository.unit_of_work():
            profile = self._repository.profile.read(uuid=shelf.profile_uuid)

        if not profile:
            raise ProfileNotFoundError(f"Profile {shelf.profile_uuid} not found.")

        gateway_items = asyncio.get_event_loop().run_until_complete(
            self._repository.gateway.shelf.items(profile, shelf)
        )

        with self._repository.unit_of_work():
            current_items = self._repository.shelf_item.search(shelf_uuid=shelf.uuid)

            result: Collate = self._repository.collate(gateway_items, current_items)

            if result:
                if result.new:
                    logger.info(f"Found {len(result.new)} new items on shelf {shelf.name}")
                    new_shelf_items: List = result.new
                    self._repository.shelf_item.create_collection(new_shelf_items)
                    logger.info(f"Created {len(result.new)} new items on shelf {shelf.name}")

                if result.deleted:
                    logger.info(f"Found {len(result.deleted)} deleted items on shelf {shelf.name}")
                    deleted_shelf_items: List = result.deleted
                    self._repository.shelf_item.delete_collection(deleted_shelf_items)
                    logger.info(f"Deleted {len(result.deleted)} items from shelf {shelf.name}")

            else:
                logger.info(f"No items changed on shelf {shelf.name}")

            shelf.refreshed_at = datetime.utcnow()
            self._repository.shelf.update(shelf)


class ScheduleShelfItemsRefreshUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    def execute(self, loop_time: int) -> List[ScheduleItem]:
        logger.info(f'Schedule refreshing items on shelves for all profiles in {loop_time}s.')

        with self._repository.unit_of_work():
            shelves: List[Shelf] = [
                shelf
                for profile in self._repository.profile.search()
                for shelf in self._repository.shelf.search(profile_uuid=profile.uuid)
            ]

        loop_step_time = int(round(loop_time / (len(shelves) + 1), 0))

        return [
            ScheduleItem(
                delay=int(idx * loop_step_time),
                args=[shelf.dict()],
            )
            for idx, shelf in enumerate(shelves)
        ]
