import logging
from domain.entities import ShelvesSearchParams, Profile
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

        profile = Profile(
            name=payload.pop('name'),
            value=payload.pop('value'),
        )

        search_results = await use_case.execute(ShelvesSearchParams(
            profile=profile,
            **payload,
        ))

        response = {
            "items": [shelf.to_dict() for shelf in search_results.items],
            "prevPage": search_results.prev_page,
            "nextPage": search_results.next_page,
        }

        return response
