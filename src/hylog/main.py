import atexit
import logging.config
import logging.handlers

from pathlib import Path

from hylog.handlers import file
from hylog.handlers import queue
from hylog.handlers import stream


def _setup_handlers(
    output_dir: Path, name: str | None = None, stdout_level: str | None = None
) -> None:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = stream.StandardOutput()
    file_last_handler = file.FileLastRun(output_dir / f"{name}_last.log")
    file_rotating_handler = file.FileRotating(output_dir / f"{name}_rotating.log")
    json_handler = file.JSONHandler(output_dir / f"{name}_json.jsonl")

    queue_handler = queue.QueueHandler()
    logger.addHandler(queue_handler)

    queue_listener = queue.QueueListener(
        stream_handler, file_last_handler, file_rotating_handler, json_handler
    )
    queue_listener.start()
    atexit.register(queue_listener.stop)


def get_app_logger(
    name: str | None = None,
    stdout_level: str | None = None,
    output_dir: str | Path | None = None,
) -> logging.Logger:
    output_dir = Path().cwd() / "logs" if output_dir is None else Path(output_dir)

    if name is None:
        name = Path().cwd().name

    _setup_handlers(output_dir, name, stdout_level)

    return logging.getLogger(name)
