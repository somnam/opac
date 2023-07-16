from sqlalchemy.orm import Mapped, mapped_column

from src.dataproviders.db.model.entity import EntityModel
from src.dataproviders.db.model.mixin import CreatedAtMixin
from src.dataproviders.db.types import Types


class ProfileModel(EntityModel, CreatedAtMixin):
    __tablename__ = "profile"

    name: Mapped[str] = mapped_column(Types.VARCHAR(512), nullable=False)
    value: Mapped[str] = mapped_column(Types.EXTERNAL_ID, nullable=False, index=True)
