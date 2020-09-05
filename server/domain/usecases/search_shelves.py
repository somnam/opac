from domain.entities import ShelvesSearchParams, ShelvesSearchResults
from data.gateways import LCGateway


class SearchShelvesUseCase:
    def __init__(self, lc_gateway: LCGateway) -> None:
        self._lc_gateway = lc_gateway

    async def execute(
        self,
        params: ShelvesSearchParams,
    ) -> ShelvesSearchResults:
        shelves = await self._lc_gateway.search_shelves(params)

        return ShelvesSearchResults(
            items=shelves,
            page=params.page,
        )
