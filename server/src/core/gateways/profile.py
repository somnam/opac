from abc import abstractmethod

from src.core.entities import ProfileSearchParams, ProfileSearchResult
from src.core.gateways.base import IGateway


class IProfileGateway(IGateway):
    @abstractmethod
    async def search(self, params: ProfileSearchParams) -> ProfileSearchResult:
        ...
