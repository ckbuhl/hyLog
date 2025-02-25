import logging.handlers
import sys

from hylog import formatters


class StandardOutput(logging.StreamHandler):
    _formatter: logging.Formatter = formatters.Simple()
    _level: int = logging.WARNING

    def __init__(self) -> None:
        super().__init__(stream=sys.stdout)
        self.setFormatter(self._formatter)
        self.setLevel(self._level)
