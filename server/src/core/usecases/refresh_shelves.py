import asyncio
import logging
from typing import List

from src.core.entities import Collate, Profile, ScheduleItem
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class RefreshShelvesUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    def execute(self, profile: Profile) -> None:
        logger.info(f'Refreshing shelves for profile {profile.name}')

        gateway_shelves = asyncio.get_event_loop().run_until_complete(
            self._repository.gateway.shelf.search(profile)
        )

        with self._repository.unit_of_work():
            current_shelves = self._repository.shelf.search(profile_uuid=profile.uuid)

            result: Collate = self._repository.collate(gateway_shelves, current_shelves)

            if result:
                if result.new:
                    logger.info(f"Found {len(result.new)} new shelves on profile {profile.name}")
                    new_shelfs: List = result.new
                    self._repository.shelf.create_collection(new_shelfs)
                    logger.info(f"Created {len(result.new)} new shelves on profile {profile.name}")

                if result.updated:
                    logger.info(f"Found {len(result.updated)} updated shelves on profile {profile.name}")
                    updated_shelfs: List = result.updated
                    self._repository.shelf.update_collection(updated_shelfs)
                    logger.info(f"Updated {len(result.updated)} shelves on profile {profile.name}")

                if result.deleted:
                    logger.info(f"Found {len(result.deleted)} deleted shelves on profile {profile.name}")
                    deleted_shelfs: List = result.deleted
                    self._repository.shelf.delete_collection(deleted_shelfs)
                    logger.info(f"Deleted {len(result.deleted)} shelves from profile {profile.name}")

            else:
                logger.info(f"No shelves changed on profile {profile.name}")


class ScheduleShelvesRefreshUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    def execute(self, loop_time: int) -> List[ScheduleItem]:
        logger.info(f'Schedule refreshing shelves for all profiles in {loop_time}s.')

        with self._repository.unit_of_work():
            profiles = list(self._repository.profile.search())

        loop_step_time = int(round(loop_time / (len(profiles) + 1), 0))

        return [
            ScheduleItem(
                delay=int(idx * loop_step_time),
                args=[profile.dict()],
            )
            for idx, profile in enumerate(profiles)
        ]
