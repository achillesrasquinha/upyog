import logging
from upyog.util.eject import ejectable
from upyog.util.cli import (
    cli_format,
    get_ansi_code
)

@ejectable(deps = ["get_logger"])
class StepLogger:
    def __init__(self, logger = None, *args, **kwargs):
        self._logger = logger or get_logger()

        self._before = kwargs.get("before")
        self._after  = kwargs.get("after")
        self._error  = kwargs.get("error")

    def __enter__(self):
        if self._before:
            self._logger.info(self._before)
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            if self._after:
                self._logger.success(self._after)
        else:
            if self._error:
                self._logger.error("%s: %s" % (self._error, value))

@ejectable()
def get_log_level(string):
    """
    Get the logging level from a string.

        Args:
            string (str): Logging level string.

        Returns:
            int: Logging level.

        Example:
            >>> get_log_level("DEBUG")
            10
    """
    import logging

    lmap = {
        "NOTSET"  : logging.NOTSET,
        "DEBUG"   : logging.DEBUG,
        "INFO"    : logging.INFO,
        "WARNING" : logging.WARNING,
        "ERROR"   : logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "SUCCESS" : 21,
        "MAGIC"   : 22
    }

    if not string in lmap:
        raise ValueError("Invalid log level: %s" % string)

    logging.addLevelName(lmap["SUCCESS"], "SUCCESS")
    logging.addLevelName(lmap["MAGIC"],   "MAGIC")

    return lmap[string]

LOGGERS = {}

@ejectable(imports = ["logging"], deps = ["get_ansi_code", "get_log_level", "cli_format"])
class LogFormatter(logging.Formatter):
    COLORS = {
        get_log_level("NOTSET")  : get_ansi_code("gray"),
        get_log_level("DEBUG")   : get_ansi_code("gray"),
        get_log_level("INFO")    : get_ansi_code("cyan"),
        get_log_level("WARNING") : get_ansi_code("yellow"),
        get_log_level("ERROR")   : get_ansi_code("red"),
        get_log_level("CRITICAL"): get_ansi_code("red"),
        get_log_level("SUCCESS") : get_ansi_code("green"),
        get_log_level("MAGIC")   : get_ansi_code("purple")
    }

    def format(self, record):
        color     = LogFormatter.COLORS[record.levelno]
        bold      = get_ansi_code("BOLD")
        format_   = cli_format('%(name)s | %(asctime)s | %(levelname)s | ', bold + color) + '%(message)s'
        formatter = logging.Formatter(format_)
        return formatter.format(record)

@ejectable(globals_ = { "LOGGERS": {} }, deps = ["get_log_level", "LogFormatter"])
def get_logger(
    name    = "default",
    level   = None,
    format_ = None
):
    """
        Get a logger instance with the given name.

        Args:
            name (str): Name of the logger.
            level (int): Log level.
            format_ (str): Log format.

        Returns:
            logging.Logger: Logger instance.

        Example:
            >>> logger = get_logger("test")
            >>> logger.info("Hello, World!")
            | default | 2021-07-01 12:00:00 | INFO | Hello, World!
    """

    import logging

    format_ = format_ or "%(asctime)s | %(levelname)s | %(message)s"
    level   = level   or get_log_level("DEBUG")

    global LOGGERS

    if not name in LOGGERS:
        formatter = LogFormatter(format_)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger  = logging.getLogger(name)
        logger.setLevel(level)

        logger.addHandler(handler)
        logger.propagate = False

        LOGGERS[name] = logger

    return LOGGERS[name]