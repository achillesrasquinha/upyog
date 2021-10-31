import os.path as osp
from threading import Lock
import json
from typing import MutableMapping

from bpyutils.util._dict  import autodict, merge_dict
from bpyutils.util.system import write, read
from bpyutils.util.string import strip

class JSONLogger(MutableMapping):
    locks = {
        "io": Lock()
    }

    def __init__(self, path, indent = 2, *args, **kwargs):
        self._path   = osp.abspath(path)
        self._indent = indent

        self._store  = autodict()
        self.update(dict(*args, **kwargs))

        self._store  = self.read()

    def read(self):
        path = self._path
        data = self._store

        if not osp.exists(path):
            if data:
                self.save()
        else:
            with self.locks['io']:
                content = read(path)
                data    = autodict(json.loads(content))

        return data

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
        store   = self._store

        with self.locks["io"]:
            if osp.exists(path):
                content = json.loads(strip(read(path)) or r"{}")
                store   = merge_dict(content, store)

            data = json.dumps(store, indent = indent)
                
            write(path, data, force = True)

    def __repr__(self):
        return str(self._store)