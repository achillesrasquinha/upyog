import functools

from collections import defaultdict

from upyog._compat import iteritems, Mapping, iterkeys, itervalues
from upyog.util.eject import ejectable
import upyog as upy

def merge_deep(source, dest):
    # https://stackoverflow.com/a/20666342
    for key, value in iteritems(source):
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            merge_deep(value, node)
        else:
            dest[key] = value
            
    return dest

def merge_dict(*args, **kwargs):
    """
    Merge Dictionaries.
    
    :param args: arguments of dictionaries to be merged. `merge_dict` will override keys from right to left.

    :returns: dict

    Example::
    
        >>> upy.merge_dict({ 'foo': 'bar' }, { 'bar': 'baz' }, { 'baz': 'boo' })
        {'foo': 'bar', 'bar': 'baz', 'baz': 'boo'}
        >>> upy.merge_dict({ 'foo': 'bar' }, { 'foo': 'baz', 'bar': 'boo' })
        {'foo': 'baz', 'bar': 'boo'}
    """
    deep = kwargs.get("deep", False)

    merged = dict()

    for arg in args:
        copy = arg.copy()

        if deep:
            merged = merge_deep(copy, merged)
        else:
            merged.update(copy)

    return merged

def dict_from_list(keys, values = None):
    """
    Generate a dictionary from a list of keys and values.

    :param keys: A list of keys.
    :param values: A list of values.

    :returns: dict

    Example::

        >>> upy.dict_from_list(['a', 'b', 'c'], [1, 2, 3])
        {'a': 1, 'b': 2, 'c': 3}
    """
    if isinstance(values, str):
        arr = keys
        key = values

        def _build_value(a, b, key):
            if key in a:
                return upy.sequencify(a[key]) + upy.sequencify(b)
            else:
                return b

        return functools.reduce(
            lambda a, b: a.update({ b[key]: _build_value(a, b, key) }) or a,
            arr, {}
        )

    if not values:
        values = [None] * len(keys)

    return dict(zip(keys, values))

class AutoDict(defaultdict):
    __repr__ = dict.__repr__

def autodict(*args, **kwargs):
    """
    Automatically adds a key to a dictionary.

    Example::

        >>> d = upy.autodict()
        >>> d['foo']['bar']['baz'] = 'boo'
        {'foo': {'bar': {'baz': 'boo'}}}
    """
    dict_type = kwargs.pop("dict_type", dict)

    _autodict = AutoDict(autodict)
    update    = dict_type(*args, **kwargs)

    for key, value in iteritems(update):
        if isinstance(value, Mapping):
            value = autodict(value)
        
        _autodict.update({
            key: value
        })
    
    return _autodict

def lkeys(d):
    """
    Get the keys of a dictionary as a list.

    :param d: A dictionary.

    :returns: list

    Example::

        >>> upy.lkeys({ 'foo': 'bar', 'baz': 'boo' })
        ['foo', 'baz']
    """
    return list(iterkeys(d))

def lvalues(d):
    """
    Get the values of a dictionary as a list.

    :param d: A dictionary.

    :returns: list

    Example::

        >>> upy.lvalues({ 'foo': 'bar', 'baz': 'boo' })
        ['bar', 'boo']
    """
    return list(itervalues(d))

def check_struct(d, struct, raise_err = True):
    """
    Check if a dictionary has a certain structure.

    :param d: A dictionary.
    :param struct: A dictionary with the structure to be checked.
    :param raise_err: Whether to raise an error if the structure is not found.

    :returns: bool

    :raises: ValueError

    :Example:

        >>> upy.check_struct({ "foo": { "bar": "baz" } }, { "foo": { "bar": str } })
        True
        >>> upy.check_struct({ "foo": { "bar": "baz" } }, { "foo": { "bar": int } }, raise_err = False)
        False
    """
    if not isinstance(d, dict):
        if raise_err:
            raise ValueError("The first argument must be a dictionary.")
        else:
            return False

    if not isinstance(struct, dict):
        if raise_err:
            raise ValueError("The second argument must be a dictionary.")
        else:
            return False

    for key, value in iteritems(struct):
        if key not in d:
            if raise_err:
                raise ValueError("The key '%s' is not in the dictionary." % key)
            else:
                return False

        if isinstance(value, dict):
            if not check_struct(d[key], value, raise_err):
                return False
        else:
            if not isinstance(d[key], value):
                if raise_err:
                    raise ValueError("The value of the key '%s' is not of type '%s'." % (key, value))
                else:
                    return False

    return d

def is_subdict(a, b):
    sub_dict = True

    for key, value in iteritems(b):
        if key in a:
            if a[key] != b[key]:
                sub_dict = False
                break

    return sub_dict

# TODO: raise exception if key not found
def getattr2(d, key, default = None):
    keys  = key.split(".")

    value = d

    for key in keys:
        if value and key in value:
            value = value[key]
        else:
            value = None

    return value or default

def hasattr2(d, key):
    return getattr2(d, key, "__missing__") != "__missing__"

@ejectable()
def setattr2(d, key, value):
    copy = d.copy()
    keys = key.split(".")

    for key in keys[:-1]:
        if key not in d:
            copy[key] = {}

        copy = copy[key]

    copy[keys[-1]] = value

    return copy

def reverse_dict(d):
    return { value: key for key, value in iteritems(d) }

_TYPE_LIST_LIKE = (list, tuple, set, frozenset)

def common_dict(a, b):
    a_keys = set(iterkeys(a))
    b_keys = set(iterkeys(b))

    common = {}

    common_keys = a_keys & b_keys
    
    for key in common_keys:
        i, j = a[key], b[key]

        if isinstance(i, Mapping) and isinstance(j, Mapping):
            common[key] = common_dict(i, j)
        elif isinstance(i, _TYPE_LIST_LIKE) and isinstance(j, _TYPE_LIST_LIKE):
            common[key] = list(set(i) & set(j))
        else:
            if i == j:
                common[key] = i

    return common

def subtract_dict(a, b):
    a_keys = set(iterkeys(a))
    b_keys = set(iterkeys(b))

    subtract = {}

    subtract_keys = a_keys - b_keys
    
    for key in subtract_keys:
        i = a[key]

        if isinstance(i, Mapping):
            subtract[key] = subtract_dict(i, {})
        elif isinstance(i, _TYPE_LIST_LIKE):
            subtract[key] = i
        else:
            subtract[key] = i

    return subtract
