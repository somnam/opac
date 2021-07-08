import requests
from src.core.gateways import ClientGatewayInterface
from src.config import Config

config = Config()


class ClientGateway(ClientGatewayInterface):
    url = config.get('client', 'url')

    def push(self, client_id: str, job_id: int, operation: str) -> None:
        requests.post(f"{self.url}/client/{client_id}/{operation}", json={"job_id": job_id})
