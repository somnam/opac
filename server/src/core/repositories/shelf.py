from abc import abstractmethod
from typing import List, Sequence

from src.core.entities import Profile, Shelf
from src.core.repositories.entity import IEntityRepository


class IShelfRepository(IEntityRepository[Shelf]):
    @abstractmethod
    async def read_all_for_profile(self, profile: Profile) -> List[Shelf]:
        ...

    @abstractmethod
    async def sync_on_profile(self, profile: Profile, shelves: Sequence[Shelf]) -> List[Shelf]:
        ...
