import asyncio
import logging
from typing import List

from src.core.entities import CollateResult, ScheduleItem, Shelf
from src.core.exceptions import ProfileNotFoundError
from src.core.repositories import DataRepositoryInterface

logger = logging.getLogger(__name__)


class RefreshShelfItemsUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    def execute(self, shelf: Shelf) -> None:
        logger.info(f'Refreshing items on shelf {shelf.name}')

        with self._repository.unit_of_work():
            profile = self._repository.profile.read(shelf.profile_id)

        if not profile:
            raise ProfileNotFoundError(f"Profile {shelf.profile_id} not found.")

        gateway_items = asyncio.run(self._repository.gateway.shelf.items(profile, shelf))

        with self._repository.unit_of_work():
            current_items = self._repository.shelf_item.read_all(shelf)

        result: CollateResult = self._repository.collate(gateway_items, current_items)

        if result:
            with self._repository.unit_of_work():

                if result.new:
                    logger.info(f"Found {len(result.new)} new items on shelf {shelf.name}")
                    new_shelf_items: List = result.new
                    self._repository.shelf_item.create_all(new_shelf_items)
                    logger.info(f"Created {len(result.new)} new items on shelf {shelf.name}")

                if result.deleted:
                    logger.info(f"Found {len(result.deleted)} deleted items on shelf {shelf.name}")
                    deleted_shelf_items: List = result.deleted
                    self._repository.shelf_item.delete_all(deleted_shelf_items)
                    logger.info(f"Deleted {len(result.deleted)} items from shelf {shelf.name}")

        else:
            logger.info(f"No items changed on shelf {shelf.name}")


class ScheduleShelfItemsRefreshUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    def execute(self, loop_time: int) -> List[ScheduleItem]:
        logger.info(f'Schedule refreshing items on shelves for all profiles in {loop_time}s.')

        with self._repository.unit_of_work():
            shelves: List[Shelf] = [
                shelf
                for profile in self._repository.profile.read_all()
                for shelf in self._repository.shelf.read_all(profile)
            ]

        loop_step_time = int(round(loop_time / (len(shelves) + 1), 0))

        return [
            ScheduleItem(
                delay=int(idx * loop_step_time),
                args=[shelf.to_dict()],
            )
            for idx, shelf in enumerate(shelves)
        ]
