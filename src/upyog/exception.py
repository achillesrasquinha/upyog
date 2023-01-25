# imports - standard imports
import subprocess as sp

class upyogError(Exception):
    pass

class PopenError(upyogError, sp.CalledProcessError):
    pass

class DependencyNotFoundError(ImportError):
    pass

class TemplateNotFoundError(upyogError):
    pass