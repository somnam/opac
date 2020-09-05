import logging
from os import path
from typing import List
from configparser import ConfigParser, ExtendedInterpolation

logger = logging.getLogger(__name__)


class Config(ConfigParser):
    app_dir: str = path.abspath(path.join(path.dirname(__file__)))
    config_files: List = ['config.ini']

    def __init__(self) -> None:
        super().__init__(
            interpolation=ExtendedInterpolation(),
        )

        # Read config file
        logger.debug(f"Reading configuration files: {self.config_files}")
        self.read([f"{self.app_dir}/{file}" for file in self.config_files])

    def optionxform(self, optionstr: str) -> str:
        """Don't lowercase keys."""
        return optionstr
