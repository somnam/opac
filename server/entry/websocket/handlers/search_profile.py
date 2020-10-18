import logging
from domain.entities import (
    ProfileSearchParams,
    ProfileSearchResults,
)
from domain.usecases import SearchProfileUseCase
from data.gateways import LCGateway
from entry.websocket.handlers.base import HandlerInterface

logger = logging.getLogger('server.entry')


class SearchProfileHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'search-profile'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchProfileUseCase(LCGateway())

        response: ProfileSearchResults = await use_case.execute(
            ProfileSearchParams(**payload)
        )

        return response.to_dict()
