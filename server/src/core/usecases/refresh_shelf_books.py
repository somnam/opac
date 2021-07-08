import asyncio
from src.core.entities import Profile, Shelf
from src.core.repositories import DataRepositoryInterface


class RefreshShelfBooksUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    async def execute(self, profile: Profile, shelf: Shelf) -> None:
        # TODO
        await asyncio.sleep(1)
