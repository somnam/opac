from abc import ABC, abstractmethod

from src.core.gateways.shelf import ShelfGatewayInterface
from src.core.gateways.profile import ProfileGatewayInterface
from src.core.gateways.client import ClientGatewayInterface


class DataGatewayInterface(ABC):

    @property
    @abstractmethod
    def shelf(self) -> ShelfGatewayInterface:
        raise NotImplementedError

    @property
    @abstractmethod
    def profile(self) -> ProfileGatewayInterface:
        raise NotImplementedError

    @property
    def client(self) -> ClientGatewayInterface:
        raise NotImplementedError
