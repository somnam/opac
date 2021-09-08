from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.entities import Profile


class ProfileRepositoryInterface(ABC):
    @abstractmethod
    def exists(self, profile_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create(self, profile: Profile) -> Profile:
        raise NotImplementedError

    @abstractmethod
    def create_all(self, profiles: List[Profile]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_all(self, profiles: List[Profile]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, profiles: List[Profile]) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self, profile_id: str) -> Optional[Profile]:
        raise NotImplementedError

    @abstractmethod
    def read_all(self) -> List[Profile]:
        raise NotImplementedError
