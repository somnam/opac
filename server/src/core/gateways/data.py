from abc import ABC, abstractmethod

from src.core.gateways.shelves import ShelvesGatewayInterface
from src.core.gateways.profiles import ProfilesGatewayInterface
from src.core.gateways.client import ClientGatewayInterface


class DataGatewayInterface(ABC):

    @property
    @abstractmethod
    def shelves(self) -> ShelvesGatewayInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def profiles(self) -> ProfilesGatewayInterface:
        raise NotImplementedError

    @property
    def client(self) -> ClientGatewayInterface:
        raise NotImplementedError
