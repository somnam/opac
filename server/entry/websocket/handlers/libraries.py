import asyncio
from entry.websocket.handlers.base import HandlerInterface


class LibrariesHandler(HandlerInterface):
    @classmethod
    def operation(cls) -> str:
        return 'libraries'

    async def execute(self, message: dict) -> dict:
        await asyncio.sleep(1)
        return {
            "libraries": [
                {
                    "name": "Kraków",
                    "value": "5004",
                },
                {
                    "name": "Bielsko-Biała",
                    "value": "4949",
                },
            ]
        }
