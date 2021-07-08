from src.core.gateways.data import DataGatewayInterface

from src.dataproviders.gateways.shelves import ShelvesGateway
from src.dataproviders.gateways.profiles import ProfilesGateway
from src.dataproviders.gateways.client import ClientGateway


class DataGateway(DataGatewayInterface):

    @property
    def shelves(self) -> ShelvesGateway:
        if not hasattr(self, "_shelves"):
            self._shelves = ShelvesGateway()
        return self._shelves

    @property
    def profiles(self) -> ProfilesGateway:
        if not hasattr(self, "_profiles"):
            self._profiles = ProfilesGateway()
        return self._profiles

    @property
    def client(self) -> ClientGateway:
        if not hasattr(self, "_client"):
            self._client = ClientGateway()
        return self._client
