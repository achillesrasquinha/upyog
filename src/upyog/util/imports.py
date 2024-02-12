from upyog.exception import DependencyNotFoundError
from upyog.util.eject import ejectable

@ejectable()
def get_handler(name):
    if '.' not in name:
        handler = __import__(name)
    else:
        module_name, handler_name = name.rsplit('.', 1)
        module  = __import__(module_name, fromlist=[handler_name])
        handler = getattr(module, handler_name)
    return handler

HANDLER_REGISTRY = {}

@ejectable(globals_ = { "HANDLER_REGISTRY": dict() }, deps = ["get_handler"])
def import_handler(name):
    """
        Import anything from module path.

        Example
        >>> from upyog.util.imports import import_handler
        >>> abspath = import_handler("os.path.abspath")
    """
    if name not in HANDLER_REGISTRY:
        HANDLER_REGISTRY[name] = get_handler(name)
    return HANDLER_REGISTRY[name]

@ejectable(deps = ["import_handler"])
def import_or_raise(package, name = None, dep = "upyog"):
    name = name or package

    try:
        return import_handler(package)
    except ImportError:
        raise DependencyNotFoundError((
            "Unable to import {package} for resolving dependencies. "
            "{dep} requires {package} to be installed. "
            "Please install {name} by executing 'pip install {name}'."
        ).format(package = package, name = name, dep = dep))