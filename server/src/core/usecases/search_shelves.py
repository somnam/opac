from src.core.entities import ShelfSearchParams, ShelfSearchResult
from src.core.repositories import IDataRepository


class SearchShelvesUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    async def execute(self, params: ShelfSearchParams) -> ShelfSearchResult:
        profile = params.profile

        with self._repository.unit_of_work():
            shelves = list(self._repository.shelf.search(profile_uuid=profile.uuid))

        if not shelves:
            shelves = list(await self._repository.gateway.shelf.search(profile))

            with self._repository.unit_of_work():
                self._repository.shelf.create_collection(shelves)

        return ShelfSearchResult(items=shelves, page=params.page)
