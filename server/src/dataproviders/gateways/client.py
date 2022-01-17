import requests

from src.config import Config
from src.core.gateways import IClientGateway

config = Config()


class ClientGateway(IClientGateway):
    _url = config.get('server', 'url')

    def push(self, client_id: str, job_id: int, operation: str) -> None:
        requests.post(f"{self._url}/client/{client_id}/{operation}", json={"job_id": job_id})
