from typing import TypeVar

from src.core.entities import Entity

__all__ = ["TEntity"]

TEntity = TypeVar("TEntity", bound=Entity)
