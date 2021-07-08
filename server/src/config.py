import json
import logging
from os import path
from typing import List, Dict, Optional, Any
from configparser import ConfigParser, ExtendedInterpolation

logger = logging.getLogger(__name__)


class Config(ConfigParser):
    app_dir: str = path.abspath(path.join(path.dirname(__file__), '..'))
    config_files: List = ['config.ini']

    def __init__(self) -> None:
        super().__init__(interpolation=ExtendedInterpolation())

        # Read config file
        logger.debug(f"Reading configuration files: {self.config_files}")
        self.read([f"{self.app_dir}/{file}" for file in self.config_files])

    def optionxform(self, optionstr: str) -> str:
        """Don't lowercase keys."""
        return optionstr

    def getstruct(self, section: str, option: str, *, raw: bool = False,
                  vars: Optional[Dict] = None, fallback: List[str] = []) -> List[str]:
        # MYPY complains about missing dynamic converter methods.
        return self._get_conv(section, option, self.struct_converter,
                              raw=raw, vars=vars, fallback=fallback)

    @staticmethod
    def struct_converter(value: str) -> Any:
        try:
            decoded_value: Any = json.loads(value)
        except json.JSONDecodeError as e:
            logger.error(f'Could not decode value "{value}": {e}')
            decoded_value = None
        return decoded_value
