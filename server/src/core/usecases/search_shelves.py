import logging
from typing import Optional

from src.core.entities import Profile, ShelfSearchParams, ShelfSearchResult
from src.core.exceptions import ProfileNotFoundError
from src.core.gateways import IDataGateway
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class SearchShelvesUseCase:
    def __init__(self, gateway: IDataGateway, repository: IDataRepository) -> None:
        self._gateway = gateway
        self._repository = repository

    async def execute(self, params: ShelfSearchParams) -> ShelfSearchResult:
        async with self._repository.context():
            profile: Optional[Profile] = await self._repository.profile.read(
                uuid=params.profile_uuid
            )
            if not profile:
                raise ProfileNotFoundError()

            shelves = await self._repository.shelf.read_all_for_profile(profile=profile)

        if not shelves:
            async with self._gateway.context():
                shelves = [shelf async for shelf in self._gateway.shelf.fetch_for_profile(profile)]

            logger.info(f"Creating {len(shelves)} new shelves on profile {profile.name}")

            async with self._repository.context():
                await self._repository.shelf.create_many(shelves)

        if params.phrase:
            shelves = [shelf for shelf in shelves if params.phrase in shelf.name]

        return ShelfSearchResult(items=shelves, page=params.page)
