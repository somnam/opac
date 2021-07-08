from abc import ABC, abstractmethod


class ClientGatewayInterface(ABC):

    @abstractmethod
    def push(self, client_id: str, job_id: str, operation: str) -> None:
        raise NotImplementedError()
