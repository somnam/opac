from src.core.gateways.shelves import ShelvesGatewayInterface
from src.core.gateways.profiles import ProfilesGatewayInterface
from src.core.gateways.data import DataGatewayInterface

from src.dataproviders.gateways.shelves import ShelvesGateway
from src.dataproviders.gateways.profiles import ProfilesGateway


class DataGateway(DataGatewayInterface):

    @property
    def shelves(self) -> ShelvesGatewayInterface:
        if not hasattr(self, "_shelves"):
            self._shelves = ShelvesGateway()
        return self._shelves

    @property
    def profiles(self) -> ProfilesGatewayInterface:
        if not hasattr(self, "_profiles"):
            self._profiles = ProfilesGateway()
        return self._profiles
