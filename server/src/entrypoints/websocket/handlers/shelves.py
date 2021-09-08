import logging

from src.core.adapters import payload_to_search_params
from src.core.entities import ShelfSearchResult
from src.core.usecases import SearchShelvesUseCase
from src.dataproviders.repositories import DataRepository
from src.entrypoints.websocket.handlers.base import HandlerInterface

logger = logging.getLogger(__name__)


class ShelvesHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'shelves'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchShelvesUseCase(DataRepository())

        search_results: ShelfSearchResult = await use_case.execute(
            payload_to_search_params(payload)
        )

        result: dict = search_results.to_dict()

        return result
