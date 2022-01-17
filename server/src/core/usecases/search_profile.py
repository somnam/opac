from src.core.entities import ProfileSearchParams, ProfileSearchResult
from src.core.repositories import IDataRepository


class SearchProfileUseCase:
    def __init__(self, repository: IDataRepository) -> None:
        self._repository = repository

    async def execute(self, params: ProfileSearchParams) -> ProfileSearchResult:
        profiles: ProfileSearchResult = await self._repository.gateway.profile.search(params)

        return profiles
