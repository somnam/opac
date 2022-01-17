import logging

from src.core.entities import Profile
from src.core.repositories import IDataRepository

logger = logging.getLogger(__name__)


class PostProfileUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    def execute(self, profile: Profile) -> None:
        with self._repository.unit_of_work():
            if not self._repository.profile.exists(uuid=profile.uuid):
                logger.info(f"Creating new profile {profile.name}")
                self._repository.profile.create(profile)
