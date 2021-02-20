import asyncio
from domain.entities import Catalog, SearchResults
from entry.websocket.handlers.base import HandlerInterface
from config import Config

config = Config()


class CatalogsHandler(HandlerInterface):

    @classmethod
    def operation(cls) -> str:
        return 'catalogs'

    async def execute(self, message: dict) -> dict:
        await asyncio.sleep(0)

        response = SearchResults(
            items=[Catalog(**entry) for entry in config.getstruct('catalogs', 'list')]
        )

        return response.to_dict()
