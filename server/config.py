import json
import logging
from os import path
from typing import List, Any
from configparser import ConfigParser, ExtendedInterpolation

logger = logging.getLogger(__name__)


class Config(ConfigParser):
    app_dir: str = path.abspath(path.join(path.dirname(__file__)))
    config_files: List = ['config.ini']

    def __init__(self) -> None:
        super().__init__(
            converters={'struct': self.struct_converter},
            interpolation=ExtendedInterpolation(),
        )

        # Read config file
        logger.debug(f"Reading configuration files: {self.config_files}")
        self.read([f"{self.app_dir}/{file}" for file in self.config_files])

    def optionxform(self, optionstr: str) -> str:
        """Don't lowercase keys."""
        return optionstr

    @staticmethod
    def struct_converter(value: str) -> Any:
        try:
            decoded_value: Any = json.loads(value)
        except json.JSONDecodeError as e:
            logger.error(f'Could not decode value "{value}": {e}')
            decoded_value = None
        return decoded_value
