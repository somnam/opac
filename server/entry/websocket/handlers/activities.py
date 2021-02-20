import asyncio
from domain.entities import Activity, SearchResults
from entry.websocket.handlers.base import HandlerInterface
from config import Config

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

        return response.to_dict()
