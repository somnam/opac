import json
import logging
import os
from configparser import ConfigParser, ExtendedInterpolation
from typing import Any, Callable, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class Config(ConfigParser):
    app_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_files: List = [
        "config.loggers.ini.example",
        "config.loggers.ini",
        "config.ini.example",
        "config.ini",
    ]

    def __init__(self) -> None:
        super().__init__(interpolation=ExtendedInterpolation())

        logger.debug(f"Reading configuration files: {self.config_files}")

        paths = [f"{self.app_dir}/{file}" for file in self.config_files]

        self.read([path for path in paths if os.path.exists(path)])

    def optionxform(self, optionstr: str) -> str:
        """Don't lowercase keys."""
        return optionstr

    def getstruct(
        self,
        section: str,
        option: str,
        *,
        raw: bool = False,
        vars: Optional[Dict] = None,
        fallback: List[str] = [],
    ) -> List[str]:
        # MYPY complains about missing dynamic converter methods.
        return self._get_conv(
            section,
            option,
            self.struct_converter,
            raw=raw,
            vars=vars,
            fallback=fallback,
        )

    def get_section(self, section: str) -> Dict:
        contents: Dict[str, Union[bool, int, float, str, Callable]] = {}

        if not self.has_section(section):
            return contents

        for option, value in self[section].items():
            if value.isnumeric():
                contents[option] = int(value)
            elif value.lower() in ("true", "false"):
                contents[option] = bool(value)
            elif self._is_float(value):
                contents[option] = float(value)
            else:
                contents[option] = value

        return contents

    @staticmethod
    def struct_converter(value: str) -> Any:
        try:
            decoded_value: Any = json.loads(value)
        except json.JSONDecodeError as e:
            logger.error(f'Could not decode value "{value}": {e}')
            decoded_value = None
        return decoded_value

    @staticmethod
    def _is_float(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
