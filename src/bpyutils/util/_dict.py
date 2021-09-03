# imports - standard imports
import collections

def merge_dict(*args):
    """
        Merge Dictionaries.
        
        :param args: arguments of dictionaries to be merged. `merge_dict` will override keys from right to left.

        Example
            >>> from bpyutils.util._dict import merge_dict
            >>> merge_dict({ 'foo': 'bar' }, { 'bar': 'baz' }, { 'baz': 'boo' })
            {'foo': 'bar', 'bar': 'baz', 'baz': 'boo'}
            >>> merge_dict({ 'foo': 'bar' }, { 'foo': 'baz', 'bar': 'boo' })
            {'foo': 'baz', 'bar': 'boo'}
    """
    merged = dict()

    for arg in args:
        copy = arg.copy()
        merged.update(copy)

    return merged

def dict_from_list(keys, values):
    return dict(zip(keys, values))

def autodict():
    _autodict = collections.defaultdict(autodict)
    return _autodict