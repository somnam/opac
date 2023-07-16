from typing import AsyncContextManager

from src.dataproviders.mixin import DbHandlerMixin


class BaseRepository(DbHandlerMixin):
    def context(self) -> AsyncContextManager:
        return self._db.session_scope()
