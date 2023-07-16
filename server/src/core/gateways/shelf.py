from abc import abstractmethod
from typing import AsyncIterator

from src.core.entities import Profile, Shelf
from src.core.gateways.base import IGateway


class IShelfGateway(IGateway):
    @abstractmethod
    def fetch_for_profile(self, profile: Profile) -> AsyncIterator[Shelf]:
        ...
