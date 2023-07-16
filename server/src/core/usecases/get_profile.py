import logging
from typing import Optional
from uuid import UUID

from src.core.entities import Profile
from src.core.exceptions import ProfileNotFoundError
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class GetProfileUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    async def execute(self, profile_uuid: UUID) -> Profile:
        async with self._repository.context():
            profile: Optional[Profile] = await self._repository.profile.read(uuid=profile_uuid)

        if not profile:
            raise ProfileNotFoundError()

        return profile
