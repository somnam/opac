from src.core.entities import ProfileSearchParams, ProfileSearchResults
from src.core.gateways import ProfilesGatewayInterface


class SearchProfileUseCase:
    def __init__(self, gateway: ProfilesGatewayInterface) -> None:
        self._gateway = gateway

    async def execute(self, params: ProfileSearchParams) -> ProfileSearchResults:
        profiles: ProfileSearchResults = await self._gateway.search(params)

        return profiles
