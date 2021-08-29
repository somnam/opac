from src.core.entities import ShelfSearchParams, ShelfSearchResult
from src.core.repositories import DataRepositoryInterface


class SearchShelvesUseCase:
    def __init__(self, repository: DataRepositoryInterface) -> None:
        self._repository = repository

    async def execute(self, params: ShelfSearchParams) -> ShelfSearchResult:
        profile = params.profile

        with self._repository.shelf.unit_of_work():
            shelves = self._repository.shelf.read_all(profile)

        if not shelves:
            shelves = await self._repository.gateway.shelf.search(profile)

            with self._repository.shelf.unit_of_work():
                self._repository.shelf.create_all(shelves)

        return ShelfSearchResult(items=shelves, page=params.page)
