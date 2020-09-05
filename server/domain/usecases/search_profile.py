from domain.entities import ProfileSearchParams, ProfileSearchResults
from data.gateways import LCGateway


class SearchProfileUseCase:
    def __init__(self, lc_gateway: LCGateway) -> None:
        self._lc_gateway = lc_gateway

    async def execute(
        self,
        params: ProfileSearchParams,
    ) -> ProfileSearchResults:
        return await self._lc_gateway.search_accounts(params)
