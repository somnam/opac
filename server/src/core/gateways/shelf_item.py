from abc import abstractmethod
from typing import AsyncIterator

from src.core.entities import Profile, Shelf, ShelfItem
from src.core.gateways.base import IGateway


class IShelfItemGateway(IGateway):
    @abstractmethod
    def fetch_for_profile_and_shelf(
        self, profile: Profile, shelf: Shelf
    ) -> AsyncIterator[ShelfItem]:
        ...
