from sqlalchemy import Column
from src.dataproviders.db.model.base import Model


class ProfileModel(Model):
    __tablename__ = "profile"

    _pk = Column(Model.BIGINT, primary_key=True)

    uuid = Column(Model.UUID, nullable=False, index=True)
    name = Column(Model.VARCHAR(512), nullable=False)
    value = Column(Model.EXTERNAL_ID, nullable=False, index=True)
