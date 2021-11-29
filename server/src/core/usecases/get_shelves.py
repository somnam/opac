import asyncio
from typing import List

from src.core.entities import Shelf
from src.core.exceptions import ProfileNotFoundError
from src.core.repositories import DataRepositoryInterface


class GetProfileShelvesUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    def execute(self, profile_id: str) -> List[Shelf]:
        with self._repository.unit_of_work():
            profile = self._repository.profile.read(profile_id)

            if not profile:
                raise ProfileNotFoundError()

            shelves = self._repository.shelf.read_all(profile)

        if not shelves:
            shelves = asyncio.run(self._repository.gateway.shelf.search(profile))

            with self._repository.unit_of_work():
                self._repository.shelf.create_all(shelves)

        return shelves
