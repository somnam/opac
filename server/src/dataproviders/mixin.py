from typing import Iterator

from src.core.entities import Collate, Entity
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


class CollateMixin:
    def collate(self, items: Iterator[Entity], current_items: Iterator[Entity]) -> Collate:

        items_set = set(items)

        current_items_set = set(current_items)

        new_items = items_set.difference(current_items_set)

        deleted_items = current_items_set.difference(items_set)

        common_items = current_items_set.intersection(items_set)

        items_map = {item: item for item in items_set}

        updated_items = {item for item in common_items if item != items_map[item]}

        return Collate(
            new=list(new_items),
            updated=list(updated_items),
            deleted=list(deleted_items),
        )
