import logging.handlers

from pathlib import Path

from hylog import formatters


class FileLastRun(logging.FileHandler):
    _formatter: logging.Formatter = formatters.Detailed()
    _mode: str = "w"
    _level: int = logging.DEBUG

    def __init__(self, filename: str | Path) -> None:
        super().__init__(filename, mode=self._mode)
        self.setLevel(self._level)
        self.setFormatter(self._formatter)




class FileRotating(logging.handlers.RotatingFileHandler):
    _formatter: logging.Formatter = formatters.Detailed()
    _level: int = logging.DEBUG
    _max_bytes: int = 3_000_000
    _backup_count: int = 3

    def __init__(self, filename: str | Path) -> None:
        super().__init__(
            filename, maxBytes=self._max_bytes, backupCount=self._backup_count
        )

        self.setLevel(self._level)
        self.setFormatter(self._formatter)


class JSONHandler(logging.handlers.RotatingFileHandler):
    _formatter: logging.Formatter = formatters.JSON()
    _level: int = logging.DEBUG
    _max_bytes: int = 3_000_000
    _backup_count: int = 3

    def __init__(self, filename: str | Path) -> None:
        super().__init__(
            filename, maxBytes=self._max_bytes, backupCount=self._backup_count
        )
        self.setLevel(self._level)
        self.setFormatter(self._formatter)
