from collections import defaultdict

from upyog._compat import iteritems, Mapping, iterkeys, itervalues

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
    
        >>> bpy.merge_dict({ 'foo': 'bar' }, { 'bar': 'baz' }, { 'baz': 'boo' })
        {'foo': 'bar', 'bar': 'baz', 'baz': 'boo'}
        >>> bpy.merge_dict({ 'foo': 'bar' }, { 'foo': 'baz', 'bar': 'boo' })
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

        >>> bpy.dict_from_list(['a', 'b', 'c'], [1, 2, 3])
        {'a': 1, 'b': 2, 'c': 3}
    """
    if not values:
        values = [None] * len(keys)

    return dict(zip(keys, values))

class AutoDict(defaultdict):
    __repr__ = dict.__repr__

def autodict(*args, **kwargs):
    """
    Automatically adds a key to a dictionary.

    Example::

        >>> d = bpy.autodict()
        >>> d['foo']['bar']['baz'] = 'boo'
        {'foo': {'bar': {'baz': 'boo'}}}
    """
    _autodict = AutoDict(autodict)
    update    = dict(*args, **kwargs)

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

        >>> bpy.lkeys({ 'foo': 'bar', 'baz': 'boo' })
        ['foo', 'baz']
    """
    return list(iterkeys(d))

def lvalues(d):
    """
    Get the values of a dictionary as a list.

    :param d: A dictionary.

    :returns: list

    Example::

        >>> bpy.lvalues({ 'foo': 'bar', 'baz': 'boo' })
        ['bar', 'boo']
    """
    return list(itervalues(d))

def check_struct(d, struct, raise_err = True):
    """
    Check if a dictionary matches a structure.

    :param d: A dictionary.
    :param struct: A dictionary structure.
    :param raise_err: Raise an error if the dictionary does not match the structure.

    :returns: bool

    Example::

        >>> upy.check_dict_struct({ 'foo': 'bar', 'baz': 'boo' }, { 'foo': str, 'baz': str })
        True
        >>> upy.check_dict_struct({ 'foo': 'bar', 'baz': 'boo' }, { 'foo': str, 'baz': int })
        False
        >>> upy.check_dict_struct({ 'foo': 'bar', 'baz': 'boo' }, { 'foo': str, 'baz': int }, raise_err = False)
        False
        >>> upy.check_dict_struct({ 'foo': 'bar', 'baz': 'boo' }, { 'foo': str, 'baz': int }, raise_err = True)
        Traceback (most recent call last):
            ...
        TypeError: 'baz' must be of type <class 'int'>, not <class 'str'>
    """
    for key, value in iteritems(struct):
        if key not in d:
            if raise_err:
                raise KeyError("'%s' is a required key" % key)
            else:
                return False

        if not isinstance(d[key], value):
            if raise_err:
                raise TypeError("'%s' must be of type %s, not %s" % (key, value, type(d[key])))
            else:
                return False

    return True