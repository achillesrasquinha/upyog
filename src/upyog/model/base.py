from upyog.util.types import classname
from upyog.util.log import get_logger, get_log_level, StepLogger
from upyog.util._dict import autodict, dict_items
from upyog.util.eject import ejectable

@ejectable(deps = ["get_logger", "get_log_level", "classname", "autodict", "StepLogger"])
class BaseObject(object):
    def __init__(self, **kwargs):
        """
            Base Object.

            Args:
                kwargs: Keyword Arguments.
        """
        for kwarg, value in dict_items(kwargs):
            setattr(self, kwarg, value)

        verbose = getattr(self, "verbose", True)

        level   = get_log_level("DEBUG") if verbose else get_log_level("INFO")
        self._logger = get_logger(self.class_name, level = level)
        self.flag    = autodict()

    @property
    def class_name(self):
        return classname(self)

    @property
    def logger(self):
        return self._logger

    def __repr__(self):
        klass  = self.class_name
        prefix = ""

        if hasattr(self, "_REPR_ATTRS"):
            attrs = getattr(self, "_REPR_ATTRS")
            for attr in attrs:
                prefix += " %s='%s'" % (attr, getattr(self, attr))

        repr_ = "<%s%s>" % (klass, prefix)
        return repr_

    def log(self, type_, message, *args, **kwargs):
        step = kwargs.pop("step", None)

        if step:
            logged = StepLogger(logger = self._logger, *args, **kwargs)
        else:
            logged = getattr(self._logger, type_)(message, *args, **kwargs)

        return logged