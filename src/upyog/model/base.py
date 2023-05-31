from upyog.util.types import classname
from upyog._compat import iteritems
from upyog import log

class BaseObject(object):
    def __init__(self, *args, **kwargs):
        for kwarg, value in iteritems(kwargs):
            setattr(self, kwarg, value)
        
        verbose = getattr(self, "verbose", True)
        self._logger = log.get_logger(self.c_name, level = log.DEBUG if verbose else log.INFO)

    @property
    def logger(self):
        return self._logger

    def __repr__(self):
        klass  = self.c_name

        prefix = ""

        if hasattr(self, "_REPR_ATTRS"):
            attrs = getattr(self, "_REPR_ATTRS")
            for attr in attrs:
                prefix += " %s='%s'" % (attr, getattr(self, attr))

        repr_ = "<%s%s>" % (klass, prefix)
        return repr_

    def log(self, type_, message, *args, **kwargs):
        getattr(self._logger, type_)(message, *args, **kwargs)

    def step_log(self, *args, **kwargs):
        return log.StepLogger(logger = self._logger, *args, **kwargs)

    @property
    def c_name(self):
        return classname(self)