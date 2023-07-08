import upyog as upy

_ejectables = {}

def _get_name(obj):
    return obj.__name__ if hasattr(obj, "__name__") else obj.__class__.__name__

def ejectable(deps = None):
    # if deps:
    #     deps = deps if isinstance(deps, (list, tuple)) else list([deps])
    #     for dep in deps:
    #         name = _get_name(dep)
    #         _ejectables[name] = dep

    def decorator(fn):
        name = _get_name(fn)
        _ejectables[name] = fn

        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper

    return decorator