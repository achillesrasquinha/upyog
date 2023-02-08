from upyog.util.types import classname
from upyog._compat import iteritems
from upyog import log

logger = log.get_logger()

class BaseObject(object):
    def __init__(self, *args, **kwargs):
        for kwarg, value in iteritems(kwargs):
            setattr(self, kwarg, value)

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
        message = "[%s] %s" % (self.c_name, message)
        getattr(logger, type_)(message, *args, **kwargs)

    @property
    def c_name(self):
        return classname(self)