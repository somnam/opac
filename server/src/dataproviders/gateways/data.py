from src.core.gateways.data import IDataGateway
from src.dataproviders.gateways.client import ClientGateway
from src.dataproviders.gateways.profile import ProfileGateway
from src.dataproviders.gateways.shelf import ShelfGateway


class DataGateway(IDataGateway):

    @property
    def shelf(self) -> ShelfGateway:
        if not hasattr(self, "_shelf"):
            self._shelf = ShelfGateway()
        return self._shelf

    @property
    def profile(self) -> ProfileGateway:
        if not hasattr(self, "_profile"):
            self._profile = ProfileGateway()
        return self._profile

    @property
    def client(self) -> ClientGateway:
        if not hasattr(self, "_client"):
            self._client = ClientGateway()
        return self._client
