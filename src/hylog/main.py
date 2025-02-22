import atexit
import json
import logging.config
import logging.handlers
import pathlib

log = logging.getLogger("hyLog")



def setup_logging() -> None:
    config_file = pathlib.Path(__file__).parent / "configs" / "stderr-json-file.json"
    with open(config_file, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)

    # Setup
    queue_handler = logging.getHandlerByName("queue_handler")
    if isinstance(queue_handler, logging.handlers.QueueHandler):
        queue_handler.listener.start()  # type: ignore
        atexit.register(queue_handler.listener.stop)  # type: ignore


def main() -> None:
    setup_logging()

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


if __name__ == "__main__":
    main()
