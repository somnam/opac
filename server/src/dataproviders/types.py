from typing import TypeVar

from src.dataproviders.db.model.entity import EntityModel

__all__ = ["TEntityModel"]

TEntityModel = TypeVar("TEntityModel", bound=EntityModel)
