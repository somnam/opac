import logging
from src.core.entities import (
    ProfileSearchParams,
    ProfileSearchResult,
)
from src.core.usecases import SearchProfileUseCase
from src.dataproviders.gateways import DataGateway
from src.entrypoints.websocket.handlers.base import HandlerInterface

logger = logging.getLogger('src.entrypoints.websocket')


class SearchProfileHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'search-profile'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchProfileUseCase(DataGateway())

        response: ProfileSearchResult = await use_case.execute(ProfileSearchParams(**payload))

        result: dict = response.to_dict()

        return result
