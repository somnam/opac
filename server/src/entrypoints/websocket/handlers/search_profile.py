import logging
from src.core.entities import (
    ProfileSearchParams,
    ProfileSearchResult,
)
from src.core.usecases import SearchProfileUseCase
from src.dataproviders.gateways import DataGateway
from src.entrypoints.websocket.handlers.base import HandlerInterface

logger = logging.getLogger(__name__)


class SearchProfileHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'search-profile'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchProfileUseCase(DataGateway())

        result: ProfileSearchResult = await use_case.execute(ProfileSearchParams(**payload))

        response: dict = result.to_dict()

        return response
