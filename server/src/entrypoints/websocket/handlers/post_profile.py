import asyncio
import logging

from src.core.entities import Profile
from src.core.usecases import PostProfileUseCase
from src.dataproviders.repositories.data import DataRepository
from src.entrypoints.websocket.handlers.base import HandlerInterface

logger = logging.getLogger(__name__)


class PostProfileHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'post-profile'

    async def execute(self, payload: dict) -> None:
        use_case = PostProfileUseCase(DataRepository())

        use_case.execute(Profile(name=payload.pop('name'), value=payload.pop('value')))

        await asyncio.sleep(0)
