# pylint: disable=E1101

# imports - compatibility imports
from bpyutils             import _compat
from bpyutils._compat     import zip
from bpyutils.util._dict  import dict_from_list

# imports - standard imports
import sys
import inspect

def get_function_arguments(fn):
    """
    Get arguments of a function.
    """
    # https://stackoverflow.com/a/2677263
    params  = dict()
    success = False
    
    if _compat.PY2: # pragma: no cover
        argspec_getter = inspect.getargspec
        success        = True
    if _compat.PYTHON_VERSION >= (3,0) and _compat.PYTHON_VERSION < (3,5): # pragma: no cover
        argspec_getter = inspect.getfullargspec
        success        = True

    if success: # pragma: no cover
        argspec   = argspec_getter(fn)
        params    = dict_from_list(argspec.args, argspec.defaults or [])

    if _compat.PYTHON_VERSION >= (3,5):
        signature  = inspect.signature(fn)
        parameters = signature.parameters

        params     = { k: v.default for k, v in _compat.iteritems(parameters) }

        success    = True

    if not success: # pragma: no cover
        raise ValueError("Unknown Python Version {} for fetching functional arguments.".format(sys.version))

    return params

def _str_to_bool(x):
    if x in ("True", "true"):
        return True
    
    if x in ("False", "false"):
        return False
    
    if x in ("None", "none", "Null", "null", "NULL", ""):
        return None

    return x

def auto_typecast(value):
    """
    Convert a string into its data type automatically.

    :param value: The value to be converted.

    Example::

        >>> bpy.auto_typecast("True")
        True
        >>> bpy.auto_typecast("1.2345")
        1.2345
    """

    for type_ in (_str_to_bool, int, float):
        try:
            return type_(value)
        except (KeyError, ValueError, TypeError):
            pass

    return value

def gen_to_seq(gen, type_ = list):
    def fn(*args, **kwargs):
        return type_(gen(*args, **kwargs))
    return fn

lfilter = gen_to_seq(filter)
lmap    = gen_to_seq(map)