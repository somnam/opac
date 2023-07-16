import logging.config

from src.config import Config
from src.dataproviders.db.handler import DbHandler

config = Config()

logging.config.fileConfig(config)


def run() -> None:
    DbHandler.create_schema()
