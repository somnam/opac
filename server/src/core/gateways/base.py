from abc import ABC, abstractmethod
from typing import AsyncContextManager


class IGateway(ABC):
    @abstractmethod
    def context(self) -> AsyncContextManager:
        ...
