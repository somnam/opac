import logging

from src.core.entities import Profile
from src.core.gateways import IDataGateway
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class RefreshShelvesUseCase:
    def __init__(self, gateway: IDataGateway, repository: IDataRepository) -> None:
        self._gateway = gateway
        self._repository = repository

    async def execute(self, profile: Profile) -> None:
        logger.info(f"Refreshing shelves for profile {profile.name}")

        async with self._gateway.context():
            remote_shelves = [
                shelf async for shelf in self._gateway.shelf.fetch_for_profile(profile)
            ]

        if not remote_shelves:
            logger.info(f"No shelves found on profile {profile.name}")
            return

        logger.info(f"Found {len(remote_shelves)} shelves on profile {profile.name}")
        async with self._repository.context():
            await self._repository.shelf.sync_on_profile(
                profile=profile,
                shelves=remote_shelves,
            )
            logger.info(f"Synchronized {len(remote_shelves)} shelves on profile {profile.name}")
