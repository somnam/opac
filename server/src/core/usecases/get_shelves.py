import logging
from typing import List

from src.core.entities import Profile, Shelf
from src.core.gateways import IDataGateway
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class GetProfileShelvesUseCase:
    def __init__(self, gateway: IDataGateway, repository: IDataRepository) -> None:
        self._gateway = gateway
        self._repository = repository

    async def execute(self, profile: Profile) -> List[Shelf]:
        async with self._repository.context():
            shelves = await self._repository.shelf.read_all_for_profile(profile)

        if not shelves:
            async with self._gateway.context():
                shelves = [shelf async for shelf in self._gateway.shelf.fetch_for_profile(profile)]

            logger.info(f"Creating {len(shelves)} new shelves on profile {profile.name}")

            async with self._repository.context():
                await self._repository.shelf.create_many(shelves)

        return shelves
