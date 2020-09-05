from abc import ABC, abstractmethod


class HandlerInterface(ABC):
    @classmethod
    @abstractmethod
    def operation(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    async def execute(self, payload: dict) -> dict:
        raise NotImplementedError
