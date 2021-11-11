import logging

from src.core.usecases import SearchProfileUseCase
from src.core.adapters import payload_to_profile_search_params
from src.dataproviders.gateways import DataGateway
from src.entrypoints.web.handlers.websocket.base import WebSocketOperationInterface

logger = logging.getLogger(__name__)


class ProfileSearchOperation(WebSocketOperationInterface):
    @classmethod
    def name(cls) -> str:
        return 'search-profile'

    async def execute(self, payload: dict) -> dict:
        use_case = SearchProfileUseCase(DataGateway())

        result = await use_case.execute(payload_to_profile_search_params(payload))

        response: dict = result.to_dict()

        return response
