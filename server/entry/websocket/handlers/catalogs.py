from domain.entities import SearchResults
from domain.usecases import GetCatalogsUseCase
from entry.websocket.handlers.base import HandlerInterface


class CatalogsHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'catalogs'

    async def execute(self, message: dict) -> dict:
        use_case = GetCatalogsUseCase()

        response: SearchResults = await use_case.execute()

        return response.to_dict()