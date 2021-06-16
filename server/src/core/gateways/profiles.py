from abc import ABC, abstractmethod

from src.core.entities import ProfileSearchParams, ProfileSearchResults


class ProfilesGatewayInterface(ABC):

    @abstractmethod
    async def search(self, params: ProfileSearchParams) -> ProfileSearchResults:
        raise NotImplementedError()
