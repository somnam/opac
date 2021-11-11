import asyncio
import logging
from typing import List

from src.core.entities import CollateResult, Profile, ScheduleItem
from src.core.repositories import DataRepositoryInterface

logger = logging.getLogger(__name__)


class RefreshShelvesUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    def execute(self, profile: Profile) -> None:
        logger.info(f'Refreshing shelves for profile {profile.name}')

        gateway_shelves = asyncio.run(self._repository.gateway.shelf.search(profile))

        with self._repository.unit_of_work():
            current_shelves = self._repository.shelf.read_all(profile)

        result: CollateResult = self._repository.collate(gateway_shelves, current_shelves)

        if result:
            with self._repository.unit_of_work():

                if result.new:
                    logger.info(f"Found {len(result.new)} new shelves on profile {profile.name}")
                    new_shelfs: List = result.new
                    self._repository.shelf.create_all(new_shelfs)
                    logger.info(f"Created {len(result.new)} new shelves on profile {profile.name}")

                if result.updated:
                    logger.info(f"Found {len(result.updated)} updated shelves on profile {profile.name}")
                    updated_shelfs: List = result.updated
                    self._repository.shelf.update_all(updated_shelfs)
                    logger.info(f"Updated {len(result.updated)} shelves on profile {profile.name}")

                if result.deleted:
                    logger.info(f"Found {len(result.deleted)} deleted shelves on profile {profile.name}")
                    deleted_shelfs: List = result.deleted
                    self._repository.shelf.delete_all(deleted_shelfs)
                    logger.info(f"Deleted {len(result.deleted)} shelves from profile {profile.name}")

        else:
            logger.info(f"No shelves changed on profile {profile.name}")


class ScheduleShelvesRefreshUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    def execute(self, loop_time: int) -> List[ScheduleItem]:
        logger.info(f'Schedule refreshing shelves for all profiles in {loop_time}s.')

        with self._repository.unit_of_work():
            profiles = self._repository.profile.read_all()

        loop_step_time = int(round(loop_time / (len(profiles) + 1), 0))

        return [
            ScheduleItem(
                delay=int(idx * loop_step_time),
                args=[profile.to_dict()],
            )
            for idx, profile in enumerate(profiles)
        ]
