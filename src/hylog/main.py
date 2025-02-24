import atexit
import json
import logging.handlers
import logging.config
import pathlib
import datetime as dt


log = logging.getLogger("hyLog")

def log_final_message() -> None:
    log.debug(f"Complete...{"\n"*2}")


def setup_logging(config_path: pathlib.Path | str) -> None:
    config_file_path = pathlib.Path(config_path)
    if not config_file_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_file_path}")

    with open(config_file_path, "r") as f:
        config = json.load(f)

    logging.config.dictConfig(config)

    # Setup thread-safe logging.
    queue_handler = logging.getHandlerByName("queue_handler")
    if isinstance(queue_handler, logging.handlers.QueueHandler):
        queue_handler.listener.start()  # type: ignore
        atexit.register(queue_handler.listener.stop)  # type: ignore
        atexit.register(log_final_message)

    log.debug("-"*80)
    log.debug(f"Logging setup complete: {dt.datetime.now()}")




if __name__ == "__main__":
    config_path = pathlib.Path(__file__).parent/ "configs" / "stderr-json-file.json"
    setup_logging(config_path)

    log.debug("DEBUG message")
    log.debug("DEBUG message with extra", extra={"extra_key": "extra_value"})
    log.info("INFO message")
    log.warning("WARNING message")
    log.error("ERROR message")
    log.critical("CRITICAL message")

    try:
        1 / 0

    except ZeroDivisionError as e:
        log.exception("Exception occurred", exc_info=e)
