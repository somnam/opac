from typing import ContextManager, Set

from src.core.entities.base import BaseEntity, CollateResult
from src.dataproviders.db import DbHandler


class DbHandlerMixin:
    @property
    def _dbh(self) -> DbHandler:
        if not hasattr(self, "_mixin_dbh"):
            self._mixin_dbh = DbHandler()
        return self._mixin_dbh

    @_dbh.setter
    def _dbh(self, dbh: DbHandler) -> None:
        self._mixin_dbh = dbh

    def unit_of_work(self) -> ContextManager:
        session_scope: ContextManager = self._dbh.session_scope()
        return session_scope


class CollateMixin:
    def collate(self, items: Set[BaseEntity], current_items: Set[BaseEntity]) -> CollateResult:

        new_items = items.difference(current_items)

        deleted_items = current_items.difference(items)

        items_map = {item: item for item in items}

        updated_items = {
            item for item in current_items.intersection(items)
            if item != items_map[item]
        }

        return CollateResult(
            new=new_items,
            updated=updated_items,
            deleted=deleted_items,
        )
