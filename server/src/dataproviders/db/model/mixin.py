from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.dataproviders.db.types import Types


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        Types.DATETIME, nullable=False, server_default=func.now()
    )


class CreatedUpdatedAtMixin(CreatedAtMixin):
    updated_at: Mapped[datetime] = mapped_column(
        Types.DATETIME, nullable=False, server_default=func.now(), onupdate=func.now()
    )
