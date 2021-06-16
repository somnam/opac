import logging
from src.core.entities import (
    ShelvesSearchParams,
    ShelvesSearchResults,
    Profile,
)
from src.core.usecases import SearchShelvesUseCase
from src.entrypoints.websocket.handlers.base import HandlerInterface
from src.dataproviders.gateways import ShelvesGateway

logger = logging.getLogger('src.entry')


class ShelvesHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'shelves'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchShelvesUseCase(ShelvesGateway())

        search_results: ShelvesSearchResults = await use_case.execute(
            ShelvesSearchParams(
                profile=Profile(name=payload.pop('name'), value=payload.pop('value')),
                **payload,
            )
        )

        result: dict = search_results.to_dict()

        return result
