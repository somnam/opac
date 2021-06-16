from abc import ABC, abstractmethod

from src.core.gateways.shelves import ShelvesGatewayInterface
from src.core.gateways.profiles import ProfilesGatewayInterface


class DataGatewayInterface(ABC):

    @property
    @abstractmethod
    def shelves(self) -> ShelvesGatewayInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def profiles(self) -> ProfilesGatewayInterface:
        raise NotImplementedError
