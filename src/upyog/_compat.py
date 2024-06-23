# imports - standard imports
import sys, os

# imports - module imports
import platform

from upyog.util.eject import ejectable

PYTHON_VERSION = sys.version_info

@ejectable()
def is_python_version(*args, **kwargs):
    """
    Determines the current Python Version.

    Args:
        major: Major Version.
        minor: Minor Version.
        micro: Patch Version.
        release: Release Level.
        serial: Serial Number.

    Returns:
        bool

    Example::
        >>> is_python_version(major = 3)
        True
        >>> is_python_version(major = 2, minor = 7)
        False
        >>> is_python_version(major = 3, minor = 6, micro = 7)
        True
    """
    import sys
    python_version = sys.version_info

    major   = kwargs.get("major")
    minor   = kwargs.get("minor")
    micro   = kwargs.get("micro")
    release = kwargs.get("release")
    serial  = kwargs.get("serial")

    result  = True

    if major:
        result = result and major   == python_version.major
    if minor:
        result = result and minor   == python_version.minor
    if micro:
        result = result and micro   == python_version.micro
    if release:
        result = result and release == python_version.releaselevel
    if serial:
        result = result and serial  == python_version.serial
        
    return result

PY2 = is_python_version(major = 2)

def cmp(a, b):
    return ((a > b) - (a < b))

@ejectable(deps = ["is_python_version"])
def iteritems(dict_, **kwargs):
    """
        Returns an iterator over the items of a dictionary.

        Args:
            dict_ (dict): Dictionary to iterate over.

        Returns:
            iterator

        Example::
            >>> dict_ = {"a": 1, "b": 2}
            >>> for key, value in iteritems(dict_):
            ...     print(key, value)
            a 1
            b 2
    """
    if is_python_version(major = 2):
        iterator = dict_.iteritems() # pragma: no cover
    else:
        iterator = iter(dict_.items(), **kwargs)
    return iterator

def iterkeys(dict_, **kwargs):
    if PY2: # pragma: no cover 
        iterator = dict_.iterkeys()
    else:
        iterator = iter(dict_.keys(), **kwargs)
    return iterator

@ejectable(deps = ["is_python_version"])
def itervalues(dict_, **kwargs):
    """
        Returns an iterator over the values of a dictionary.

        Args:
            dict_ (dict): Dictionary to iterate over.
            
        Returns:
            iterator

        Example::
            >>> dict_ = {"a": 1, "b": 2}
            >>> for value in itervalues(dict_):
            ...     print(value)
            1
            2
    """
    if is_python_version(major = 2): # pragma: no cover
        iterator = dict_.itervalues()
    else:
        iterator = iter(dict_.values(), **kwargs)
    return iterator

if PYTHON_VERSION < (3,6): # pragma: no cover
    class ModuleNotFoundError(ImportError):
        pass
else:
    ModuleNotFoundError = ModuleNotFoundError

if PYTHON_VERSION > (3,8): # pragma: no cover
    from collections.abc    import Iterable
else:
    from collections        import Iterable

if PY2: # pragma: no cover
    # moves
    from urllib2  import urlopen, Request
    from urlparse import urlparse, urljoin
    from urllib   import quote
    
    try:
        from requests.exceptions import HTTPError
    except ImportError:
        from urllib2 import HTTPError

    from urllib  import urlencode

    import __builtin__ as builtins

    from __builtin__ import raw_input as input

    from StringIO import StringIO
    from BytesIO  import BytesIO

    from itertools import izip         as zip
    from itertools import izip_longest as zip_longest

    import ConfigParser as configparser

    string_types = basestring
    
    range        = xrange

    from Queue import Queue

    from collections import (
        Mapping,
        Sequence
    )
else:
    # moves
    from urllib.request import urlopen, Request
    from urllib.parse   import urlencode, urlparse, urljoin, quote

    try:
        from requests.exceptions import HTTPError
    except (ImportError, ModuleNotFoundError):
        from urllib.error   import HTTPError

    import builtins

    from builtins import input, range

    from io import StringIO, BytesIO

    from itertools import zip_longest

    zip = zip

    import configparser

    string_types = str

    from queue import Queue

    from collections.abc import (
        Mapping,
        Sequence
    )
    
if platform.system() in ['Linux', 'Darwin']:
    EX_OK      = os.EX_OK
    EX_NOINPUT = os.EX_NOINPUT
else: # pragma: no cover
    EX_OK      = 0
    EX_NOINPUT = 66