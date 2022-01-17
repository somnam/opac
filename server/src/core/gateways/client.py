from abc import ABC, abstractmethod


class IClientGateway(ABC):

    @abstractmethod
    def push(self, client_id: str, job_id: int, operation: str) -> None:
        raise NotImplementedError()
