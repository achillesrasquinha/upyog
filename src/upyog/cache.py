import os, os.path as osp

import upyog
from   upyog.util.system import makedirs
from   upyog.util._aws import is_lambda

class Cache:
    def __init__(self, location = None, dirname = None):
        basedir = osp.expanduser("~") if not is_lambda() else "/tmp"
        self.location = location or osp.join(basedir, ".config")
        self.dirname  = dirname  or upyog.__name__

    @property
    def path(self):
        return osp.join(self.location, self.dirname)

    def create(self, exist_ok = True):
        path = self.path
        makedirs(path, exist_ok = exist_ok)