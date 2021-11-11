from sqlalchemy import Column
from src.dataproviders.db.model.base import Model


class ShelfModel(Model):
    __tablename__ = "shelf"

    _pk = Column(Model.BIGINT, primary_key=True)

    shelf_id = Column(Model.MD5, nullable=False, index=True)
    profile_id = Column(Model.MD5, nullable=False, index=True)
    name = Column(Model.VARCHAR(512), nullable=False)
    value = Column(Model.EXTERNAL_ID, nullable=False)
    pages = Column(Model.INT, nullable=False)
    refreshed_at = Column(Model.DATETIME, nullable=True)
