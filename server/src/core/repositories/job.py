from abc import ABC, abstractmethod
from typing import Any, Callable, Optional


class JobRepositoryInterface(ABC):
    queue: Any = None

    @abstractmethod
    def exists(self, job_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def enqueue(self, job: Callable, meta: Optional[dict] = None, args: Any = None, kwargs: Any = None) -> int:
        raise NotImplementedError()

    @abstractmethod
    def finished(self, job_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def result(self, job_id: int) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def operation(self, job_id: int) -> Optional[str]:
        raise NotImplementedError()
