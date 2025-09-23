import io
from multiprocessing import get_context
from multiprocessing.queues import Queue

import pytest

from loggink.formatter import MessageFormatter
from loggink.handler import StreamHandler
from loggink.logger import Logger
from loggink.util import LogItem


## Capturing logging messages
class CapLogger(Logger):
    """Logging class for capturing texting logging."""

    @property
    def text(self) -> str:
        stream = self._handlers[0].stream
        stream.seek(0)
        return stream.read()


@pytest.fixture
def log_capture() -> io.StringIO:
    buffer = io.StringIO()
    return buffer


@pytest.fixture
def caplog(log_capture: io.StringIO) -> Logger:
    logger = CapLogger("fiat")
    logger._handlers = []
    logger.add_stream_handler(name="Capture", level=2, stream=log_capture)
    return logger


## Single objects for logging testing
@pytest.fixture(scope="session")
def formatter() -> MessageFormatter:
    mf = MessageFormatter(fmt="{levelname:8s}{message}")
    return mf


@pytest.fixture
def log_item() -> LogItem:
    l = LogItem(2, "A logging message")
    return l


@pytest.fixture
def mp_queue() -> Queue:
    ctx = get_context()
    q = Queue(ctx=ctx, maxsize=2)
    return q


@pytest.fixture
def stream_capture(log_capture: io.StringIO) -> StreamHandler:
    h = StreamHandler(level=2, stream=log_capture, name="stream")
    return h
