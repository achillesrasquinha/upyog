from __future__ import absolute_import

# imports - standard imports
import logging
import time

# imports - module imports
from upyog._compat     import iteritems
from upyog.util.string import ellipsis
from upyog.util.log    import get_logger
from upyog.util.eject  import ejectable

NOTSET      = logging.NOTSET
DEBUG       = logging.DEBUG
INFO        = logging.INFO
WARNING     = logging.WARNING
ERROR       = logging.ERROR
CRITICAL    = logging.CRITICAL

SUCCESS     = 21
logging.addLevelName(SUCCESS, "SUCCESS")
MAGIC       = 22
logging.addLevelName(MAGIC,   "MAGIC")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)

def magic(self, message, *args, **kwargs):
    if self.isEnabledFor(MAGIC):
        self._log(MAGIC, message, args, **kwargs)

logging.Logger.success = success
logging.Logger.magic   = magic

def _log(self, level, msg, *args, **kwargs):
    logs = getattr(self, "_logs", [])
    logs.append((time, level, msg, args, kwargs))

    if len(logs) > self.max_log_history:
        logs.pop(0)
        self._logs = logs

    super_ = super(logging.Logger, self)
    super_._log(level, msg, *args, **kwargs)

def log_fn(fn):
    logger = get_logger(fn.__module__ + "." + fn.__name__)
    
    def wrapper(*args, **kwargs):
        magstr = "%s: (%s, %s)" % (fn.__name__, args, { k: ellipsis(str(v), 50) for k, v in iteritems(kwargs) })
        logger.magic(magstr)
        return fn(*args, **kwargs)

    return wrapper