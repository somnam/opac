import logging

from src.core.entities import Profile
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class CreateProfileUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    async def execute(self, profile: Profile) -> None:
        async with self._repository.context():
            if await self._repository.profile.exists(uuid=profile.uuid):
                logger.info(f"Profile {profile.name} exists")
                return

            logger.info(f"Creating new profile {profile.name}")
            await self._repository.profile.create(profile)
