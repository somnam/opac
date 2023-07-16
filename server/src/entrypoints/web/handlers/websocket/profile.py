import logging

from src.core.transforms import payload_to_profile_search_params
from src.core.usecases import SearchProfileUseCase
from src.dataproviders.gateways import DataGateway
from src.entrypoints.web.handlers.websocket.base import IWebSocketOperation

logger = logging.getLogger(__name__)


class ProfileSearchOperation(IWebSocketOperation):
    @classmethod
    def name(cls) -> str:
        return "search-profile"

    async def execute(self, payload: dict) -> dict:
        use_case = SearchProfileUseCase(gateway=DataGateway())

        result = await use_case.execute(payload_to_profile_search_params(payload))

        response: dict = result.dict()

        return response
