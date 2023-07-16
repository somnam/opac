import logging

from src.core.entities import ShelfSearchResult
from src.core.transforms import payload_to_shelf_search_params
from src.core.usecases import SearchShelvesUseCase
from src.dataproviders.gateways import DataGateway
from src.dataproviders.repositories import DataRepository
from src.entrypoints.web.handlers.websocket.base import IWebSocketOperation

logger = logging.getLogger(__name__)


class ShelvesOperation(IWebSocketOperation):
    @classmethod
    def name(cls) -> str:
        return "shelves"

    async def execute(self, payload: dict) -> dict:
        use_case = SearchShelvesUseCase(repository=DataRepository(), gateway=DataGateway())

        search_params = payload_to_shelf_search_params(payload)

        search_results: ShelfSearchResult = await use_case.execute(search_params)

        result: dict = search_results.dict()

        return result
