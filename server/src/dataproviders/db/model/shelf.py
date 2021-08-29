from sqlalchemy import Column
from src.dataproviders.db.model.base import Model


class ShelfModel(Model):
    __tablename__ = "shelf"

    _pk = Column(Model.BIGINT, primary_key=True)

    name = Column(Model.VARCHAR(512), nullable=False)
    value = Column(Model.EXTERNAL_ID, nullable=False)
    profile_value = Column(Model.MD5, nullable=False, index=True)
    pages = Column(Model.INT, nullable=False)
