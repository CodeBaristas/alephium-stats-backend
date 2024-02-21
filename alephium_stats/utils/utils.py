import datetime as dt
import logging
import sys
import traceback
from functools import wraps

import pytz
from dimfred import Stopwatch
from loguru import logger


################################################################################
# LOGGER
class InterceptHandler(logging.Handler):  # pragma: no cover
    def __init__(self):
        super().__init__()

    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init_logger(level, ignore=[]):  # pragma: no cover
    # intercept logs from default logging module
    logging.basicConfig(handlers=[InterceptHandler()], level=1, force=True)

    # clear the config
    logger.remove()

    # ignore some entries
    for entry in ignore:
        logger.disable(entry)

    # validate that the level is correct
    levels = ("DEBUG", "INFO", "WARNING", "ERROR")
    if level not in levels:
        raise ValueError(f"Unknown log level: {level}\nAllowed Values: {levels}")

    # attach this and all above layers
    logger.add(sys.stderr, level=level)


def log_time(logger):  # pragma: no cover
    def deco(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            sw = Stopwatch()
            res = f(*args, **kwargs)
            logger.info(f"{f.__name__} took: {sw()}")

            return res

        return wrapper

    return deco


def exception(e):  # pragma: no cover
    einfo = "".join(traceback.format_exception(type(e), value=e, tb=e.__traceback__))
    return logger.error(einfo)


setattr(logger, "exception", exception)
# TODO maybe later pretty printing pydantic objs
# setattr(logger, "pinfo", lambda o: logger.info(Pretty(o)))


################################################################################
# TIME
def utc(t):  # pragma: no cover
    return t.replace(tzinfo=pytz.UTC)


def utcnow():  # pragma: no cover
    return dt.datetime.now(dt.timezone.utc)


def timestamp():  # pragma: no cover
    return int(utcnow().timestamp())


def stime(datetime):  # pragma: no cover
    s = str(datetime)
    s, _ = s.split("+")
    s = s.replace(" ", "T")

    return s


def time_frontend(datetime):  # pragma: no cover
    return str(datetime).split(".")[0]
