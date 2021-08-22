from src.core.entities import ProfileSearchParams, ProfileSearchResult
from src.core.gateways import DataGatewayInterface


class SearchProfileUseCase:
    def __init__(self, gateway: DataGatewayInterface) -> None:
        self._gateway = gateway

    async def execute(self, params: ProfileSearchParams) -> ProfileSearchResult:
        profiles: ProfileSearchResult = await self._gateway.profile.search(params)

        return profiles
