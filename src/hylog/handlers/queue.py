import logging.handlers

from multiprocessing import Queue


log_queue = Queue(-1)

class QueueHandler(logging.handlers.QueueHandler):
    def __init__(self) -> None:
        super().__init__(log_queue)

class QueueListener(logging.handlers.QueueListener):
    def __init__(self, *handlers: logging.Handler) -> None:
        super().__init__(log_queue, *handlers, respect_handler_level=True)