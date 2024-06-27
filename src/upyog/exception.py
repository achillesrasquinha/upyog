# imports - standard imports
import subprocess as sp
from upyog.util.eject import ejectable

class UpyogError(Exception):
    pass

class PopenError(UpyogError, sp.CalledProcessError):
    pass

@ejectable()
class DependencyNotFoundError(ImportError):
    pass

class TemplateNotFoundError(UpyogError):
    pass