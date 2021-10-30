import os.path as osp
from collections import MutableMapping
from threading import Lock
import json

from bpyutils.util._dict  import autodict
from bpyutils.util.system import write, read

class JSONLogger(MutableMapping):
    locks = {
        "io": Lock()
    }

    def __init__(self, path, indent = 2, *args, **kwargs):
        self._path   = path
        self._indent = indent

        self._store  = autodict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        value = self._store[key]
        return value

    def __setitem__(self, key, value):
        self._store[key] = value
        self.save()

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def save(self):
        path    = self._path
        indent  = self._indent

        data    = json.dumps(self._store, indent = indent)

        with self.locks["io"]:
            write(path, data)