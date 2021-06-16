import logging
from src.core.entities import (
    ProfileSearchParams,
    ProfileSearchResults,
)
from src.core.usecases import SearchProfileUseCase
from src.dataproviders.gateways import ProfilesGateway
from src.entrypoints.websocket.handlers.base import HandlerInterface

logger = logging.getLogger('src.entry')


class SearchProfileHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'search-profile'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchProfileUseCase(ProfilesGateway())

        response: ProfileSearchResults = await use_case.execute(ProfileSearchParams(**payload))

        result: dict = response.to_dict()

        return result
