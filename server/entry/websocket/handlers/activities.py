from domain.entities import SearchResults
from domain.usecases import GetActivitiesUseCase
from entry.websocket.handlers.base import HandlerInterface


class ActivitiesHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'activities'

    async def execute(self, message: dict) -> dict:
        use_case = GetActivitiesUseCase()

        response: SearchResults = await use_case.execute()

        return response.to_dict()
