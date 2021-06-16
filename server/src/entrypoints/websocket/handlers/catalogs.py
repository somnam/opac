import asyncio
from src.core.entities import Catalog, SearchResults
from src.entrypoints.websocket.handlers.base import HandlerInterface
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

        result: dict = response.to_dict()

        return result
