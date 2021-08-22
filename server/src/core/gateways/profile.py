from abc import ABC, abstractmethod

from src.core.entities import ProfileSearchParams, ProfileSearchResult


class ProfileGatewayInterface(ABC):

    @abstractmethod
    async def search(self, params: ProfileSearchParams) -> ProfileSearchResult:
        raise NotImplementedError()
