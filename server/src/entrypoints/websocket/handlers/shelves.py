import logging
from src.core.entities import (
    ShelfSearchParams,
    ShelfSearchResult,
    Profile,
)
from src.core.usecases import SearchShelvesUseCase
from src.entrypoints.websocket.handlers.base import HandlerInterface
from src.dataproviders.repositories import DataRepository

logger = logging.getLogger('src.entrypoints.websocket')


class ShelvesHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'shelves'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchShelvesUseCase(DataRepository())

        search_results: ShelfSearchResult = await use_case.execute(
            ShelfSearchParams(
                profile=Profile(name=payload.pop('name'), value=payload.pop('value')),
                **payload,
            )
        )

        result: dict = search_results.to_dict()

        return result
