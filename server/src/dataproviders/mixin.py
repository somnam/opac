from typing import ContextManager

from src.dataproviders.db import DbHandler


class DbHandlerMixin:
    @property
    def _dbh(self) -> DbHandler:
        if not hasattr(self, "_mixin_dbh"):
            self._mixin_dbh = DbHandler()
        return self._mixin_dbh

    def unit_of_work(self) -> ContextManager:
        return self._dbh.session_scope()