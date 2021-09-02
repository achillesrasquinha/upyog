# imports - standard imports
import subprocess as sp

class BpyutilsError(Exception):
    pass

class PopenError(BpyutilsError, sp.CalledProcessError):
    pass

class DependencyNotFoundError(ImportError):
    pass