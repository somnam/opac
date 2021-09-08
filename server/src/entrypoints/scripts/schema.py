import logging.config

from src.dataproviders.db.handler import DbHandler
from src.config import Config

config = Config()

logging.config.fileConfig(config)


def run() -> None:
    DbHandler.create_schema()
