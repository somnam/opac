from src.core.entities import ShelfSearchParams, ShelfSearchResult
from src.core.gateways import DataGatewayInterface


class SearchShelvesUseCase:
    def __init__(self, gateway: DataGatewayInterface) -> None:
        self._gateway = gateway

    async def execute(self, params: ShelfSearchParams) -> ShelfSearchResult:
        shelves = await self._gateway.shelf.search(params.profile)

        return ShelfSearchResult(items=shelves, page=params.page)
