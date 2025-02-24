import logging.handlers
import sys

from hylog import formatters


class StandardOutput(logging.StreamHandler):
    _formatter: logging.Formatter = formatters.Simple()

    def __init__(self) -> None:
        super().__init__(stream=sys.stdout)
        self.setFormatter(self._formatter)
