# pylint: disable=E1101
from functools import partial

# imports - compatibility imports
from upyog import _compat
from upyog._compat import iteritems, iterkeys, itervalues, Mapping
from upyog.util._dict import dict_from_list
from upyog.util.datetime import auto_datetime
from upyog.util.eject import ejectable

# imports - standard imports
import sys
import inspect

def get_function_arguments(fn):
    """Get arguments of a function

    Args:
        fn (function): The function to retrieve arguments from.

    Returns:
        dict: A dictionary of arguments. If there is no default argument, the value 
        associated to that argument would be inpsect._empty.

    Example

        >>> def add(a = 0, b = 1):
                return a + b
        >>> params = upy.get_function_arguments(add)
        >>> params
        {'a': 0, 'b': 1}
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

# def _str_to_bool(x):
#     if x in ("True", "true"):
#         return True
    
#     if x in ("False", "false"):
#         return False
    
#     if x in ("None", "none", "Null", "null", "NULL", ""):
#         return None

#     return x

@ejectable()
def auto_typecast(value):
    """
    Automatically convert a string into its desired data type.

    :param value: The value to be converted.

    Example::

        >>> upy.auto_typecast("True")
        True
        >>> upy.auto_typecast("1.2345")
        1.2345
    """
    str_to_bool = lambda x: { "True": True, "False": False, "None": None}[x]

    for type_ in (str_to_bool, int, float, auto_datetime):
        try:
            return type_(value)
        except (KeyError, ValueError, TypeError):
            pass

    return value

@ejectable()
def _gen_to_seq(gen, type_ = list):
    def fn(*args, **kwargs):
        return type_(gen(*args, **kwargs))
    return fn

@ejectable(deps = ["check_array"])
def filter2(fn, arr):
    if not callable(fn):
        if check_array(fn, raise_err = False):
            l  = fn
            fn = lambda x: x not in l
        else:
            fn = lambda x: x != fn

    return filter(fn, arr)

@ejectable(deps = ["_gen_to_seq", "filter2"])
def lfilter(fn, arr):
    return _gen_to_seq(filter2)(fn, arr)

@ejectable(deps = ["_gen_to_seq"])
def lmap(fn, arr):
    return _gen_to_seq(map)(fn, arr)

@ejectable(deps = ["_gen_to_seq"])
def lset(arr):
    return _gen_to_seq(set)(arr)

@ejectable()
def build_fn(fn, *args, **kwargs):
    """Build a function caller with default arguments.

    Args:
        fn (function): The function to be called.

    Returns:
        function: A function wrapper with default arguments passed.

    Example:
        
        >>> def add(a, b):
                return a + b
        >>> fn = upy.build_fn(add, a = 1, b = 2)
        >>> fn()
        3
    """
    from functools import partial
    return partial(fn, *args, **kwargs)

@ejectable()
def check_array(o, raise_err = True):
    """
    Check if an object is an array.

    :param o: The object to be checked.
    :param raise_err: If True, raises an error if the object is not an array.

    Example::

        >>> upy.check_array([1, 2, 3])
        True
        >>> upy.check_array(1)
        False
    """
    if isinstance(o, (list, tuple, set)):
        return True
    else:
        if raise_err:
            raise TypeError("Object is not an array.")
        else:
            return False

@ejectable()
def classname(obj):
    """
    Get the name of a class.

    :param obj: The object to get the name of.

    Example::

        >>> upy.classname("Hello World")
        'str'
        >>> upy.classname(1)
        'int'
    """
    return obj.__class__.__name__

@ejectable()
def is_num_like(x):
    """
    Check if an object is numeric.

    :param x: The object to be checked.

    Example::

        >>> upy.is_num_like(1)
        True
        >>> upy.is_num_like("Hello World")
        False
        >>> upy.is_num_like("1")
        True
    """
    if isinstance(x, str):
        return x.isdigit()
    elif isinstance(x, (int, float)):
        return True
    
    return False

@ejectable()
def is_dict_like(x):
    """
    Check if an object is a dictionary.

    :param x: The object to be checked.

    Example::

        >>> upy.is_dict_like({ "foo": "bar" })
        True
        >>> upy.is_dict_like([1, 2, 3])
        False
    """
    return isinstance(x, Mapping)

@ejectable()
def ordered(x):
    if isinstance(x, dict):
        return sorted((k, ordered(v)) for k, v in iteritems(x))
    elif isinstance(x, list):
        return sorted(ordered(v) for v in x)
    
    return x

@ejectable()
def to_object(d):
    class O(object):
        pass

    params = O()

    for k, v in iteritems(d):
        setattr(params, k, v)

    return params

@ejectable()
def combinations(options):
    import itertools
    return [
        dict(zip(iterkeys(options), value)) for value in itertools.product(*itervalues(options))
    ]