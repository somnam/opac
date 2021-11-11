import logging

from src.core.adapters import payload_to_shelf_search_params
from src.core.entities import ShelfSearchResult
from src.core.usecases import SearchShelvesUseCase
from src.dataproviders.repositories import DataRepository
from src.entrypoints.web.handlers.websocket.base import WebSocketOperationInterface

logger = logging.getLogger(__name__)


class ShelvesOperation(WebSocketOperationInterface):
    @classmethod
    def name(cls) -> str:
        return 'shelves'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchShelvesUseCase(DataRepository())

        search_params = payload_to_shelf_search_params(payload)

        search_results: ShelfSearchResult = await use_case.execute(search_params)

        result: dict = search_results.to_dict()

        return result
