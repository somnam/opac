from abc import ABC, abstractmethod
from typing import Optional


class WebSocketOperationInterface(ABC):
    client_id: None

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    async def execute(self, payload: dict) -> Optional[dict]:
        raise NotImplementedError
