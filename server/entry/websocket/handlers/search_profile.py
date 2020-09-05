import logging
from domain.entities import ProfileSearchParams
from domain.usecases import SearchProfileUseCase
from data.gateways import LCGateway
from entry.websocket.handlers.base import HandlerInterface

logger = logging.getLogger('server.entry')


class SearchProfileHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'search_profile'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchProfileUseCase(LCGateway())

        search_results = await use_case.execute(ProfileSearchParams(**payload))

        response = {
            "items": [profile.to_dict() for profile in search_results.items],
            "prevPage": search_results.prev_page,
            "nextPage": search_results.next_page,
        }

        return response
