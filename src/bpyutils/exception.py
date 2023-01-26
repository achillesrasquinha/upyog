# imports - standard imports
import subprocess as sp

class UpyogError(Exception):
    pass

class PopenError(UpyogError, sp.CalledProcessError):
    pass

class DependencyNotFoundError(ImportError):
    pass