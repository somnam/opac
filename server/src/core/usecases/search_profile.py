from src.core.entities import ProfileSearchParams, ProfileSearchResults
from src.core.gateways import DataGatewayInterface


class SearchProfileUseCase:
    def __init__(self, gateway: DataGatewayInterface) -> None:
        self._gateway = gateway

    async def execute(self, params: ProfileSearchParams) -> ProfileSearchResults:
        profiles: ProfileSearchResults = await self._gateway.profiles.search(params)

        return profiles
