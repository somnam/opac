from typing import List
from domain.entities import Catalog
from domain.usecases import GetCatalogsUseCase
from entry.websocket.handlers.base import HandlerInterface


class CatalogsHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'catalogs'

    async def execute(self, message: dict) -> dict:
        use_case = GetCatalogsUseCase()

        catalogs: List[Catalog] = await use_case.execute()

        return {"catalogs": [catalog.to_dict() for catalog in catalogs]}
