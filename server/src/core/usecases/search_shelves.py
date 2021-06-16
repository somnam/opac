from src.core.entities import ShelvesSearchParams, ShelvesSearchResults
from src.core.gateways import ShelvesGatewayInterface


class SearchShelvesUseCase:
    def __init__(self, gateway: ShelvesGatewayInterface) -> None:
        self._gateway = gateway

    async def execute(self, params: ShelvesSearchParams) -> ShelvesSearchResults:
        shelves = await self._gateway.search(params)

        return ShelvesSearchResults(
            items=shelves,
            page=params.page,
        )
