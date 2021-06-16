import asyncio

from config import Config
from src.core.entities import Activity, SearchResults
from src.entrypoints.websocket.handlers.base import HandlerInterface

config = Config()


class ActivitiesHandler(HandlerInterface):

    @classmethod
    def operation(cls) -> str:
        return 'activities'

    async def execute(self, message: dict) -> dict:
        await asyncio.sleep(0)

        response = SearchResults(
            items=[Activity(**entry) for entry in config.getstruct('activities', 'list')]
        )

        result: dict = response.to_dict()

        return result
