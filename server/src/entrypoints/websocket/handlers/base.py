from abc import ABC, abstractmethod
from typing import Optional


class HandlerInterface(ABC):
    client_id: None

    @classmethod
    @abstractmethod
    def operation(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    async def execute(self, payload: dict) -> Optional[dict]:
        raise NotImplementedError
