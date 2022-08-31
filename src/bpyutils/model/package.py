import os.path as osp

from bpyutils.model.base import BaseObject

class Package(BaseObject):
    def __init__(self, path = None):
        if path:
            if not osp.exists(path):
                raise FileNotFoundError("Package at path %s not found." % path)

            self._path = osp.abspath(path)
    
    def from_path(path):
        return Package(path = path)