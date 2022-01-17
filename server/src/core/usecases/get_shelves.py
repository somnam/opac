import logging
from typing import List
from uuid import UUID

from src.core.entities import Shelf
from src.core.exceptions import ProfileNotFoundError
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class GetProfileShelvesUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    async def execute(self, profile_uuid: UUID) -> List[Shelf]:
        with self._repository.unit_of_work():
            profile = self._repository.profile.read(uuid=profile_uuid)

            if not profile:
                raise ProfileNotFoundError()

            shelves = list(self._repository.shelf.search(profile_uuid=profile.uuid))

        if not shelves:
            shelves = list(await self._repository.gateway.shelf.search(profile))

            logger.info(f"Creating {len(shelves)} new shelves on profile {profile.name}")

            with self._repository.unit_of_work():
                self._repository.shelf.create_collection(shelves)

        return shelves
