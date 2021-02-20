import logging
from domain.entities import (
    ShelvesSearchParams,
    ShelvesSearchResults,
    Profile,
)
from domain.usecases import SearchShelvesUseCase
from entry.websocket.handlers.base import HandlerInterface
from data.gateways import LCGateway

logger = logging.getLogger('server.entry')


class ShelvesHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'shelves'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchShelvesUseCase(LCGateway())

        search_results: ShelvesSearchResults = await use_case.execute(
            ShelvesSearchParams(
                profile=Profile(name=payload.pop('name'), value=payload.pop('value')),
                **payload,
            )
        )

        return search_results.to_dict()
