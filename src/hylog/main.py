import atexit
import datetime as dt
import json
import logging.config
import logging.handlers
from pathlib import Path

class _LoggerMetadata:
    config_path: Path = Path(__file__).parent / "configs" / "default.json"
    name: str = str(Path().cwd().parent)
    output_dir: Path = Path().cwd() / "logs"

    formatters: set[str] = set()
    file_handlers: set[str] = set()

def _configure_from_defaults() -> None:
    with open(_LoggerMetadata.config_path, "r") as f:
        config: dict[str, str] = json.load(f)

    logging.config.dictConfig(config)
    
    _LoggerMetadata.file_handlers = set(file_handlers)

    # Setup thread-safe logging using the QueueHandler.
    queue_handler = logging.getHandlerByName("queue_handler")
    if isinstance(queue_handler, logging.handlers.QueueHandler):
        queue_handler.listener.start()  # type: ignore
        atexit.register(queue_handler.listener.stop)  # type: ignore

def _set_logger_name(name: str | None) -> None:
    if name is not None:
        _LoggerMetadata.name = name
    else:
        _LoggerMetadata.name = str(Path().cwd().parent)


def _set_output_dir(output_dir: str | Path | None) -> None:
    if output_dir is not None and Path.is_dir(Path(output_dir)):
        _LoggerMetadata.output_dir = Path(output_dir)

    else:


def _set_stdout_level(level: str) -> None:
    stream_handler = logging.getHandlerByName("stdout")
    if stream_handler is not None:
        stream_handler.setLevel(level)



def get_app_logger(name: str | None, stdout_level: str | None = None, output_dir: str | Path | None = None) -> logging.Logger:
    _configure_from_defaults()
    _set_logger_name(name)
    _set_output_dir(output_dir)



    if stdout_level is not None:
        _set_stdout_level(stdout_level)





    return logging.getLogger(name)
