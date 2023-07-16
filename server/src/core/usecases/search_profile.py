import logging

from src.core.entities import ProfileSearchParams, ProfileSearchResult
from src.core.gateways import IDataGateway

logger = logging.getLogger(__name__)


class SearchProfileUseCase:
    def __init__(self, gateway: IDataGateway) -> None:
        self._gateway = gateway

    async def execute(self, params: ProfileSearchParams) -> ProfileSearchResult:
        async with self._gateway.context():
            logger.info(f"Search profile containing '{params.phrase}'")
            profiles = await self._gateway.profile.search(params)

        return profiles
