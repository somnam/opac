from typing import ContextManager

from src.core.repositories.base import IRepository
from src.dataproviders.mixin import CollateMixin, DbHandlerMixin


class BaseDbRepository(DbHandlerMixin, CollateMixin, IRepository):

    def unit_of_work(self) -> ContextManager:
        session_scope: ContextManager = self._dbh.session_scope()
        return session_scope
