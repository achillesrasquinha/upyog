import upyog as upy

_ejectables = {}

def _get_name(obj):
    return obj.__name__ if hasattr(obj, "__name__") else obj.__class__.__name__

def ejectable(deps = None, globals_ = None, sources = None, as_ = None, alias = None,
    imports = None):
    if imports:
        imports = imports if isinstance(imports, (list, tuple)) else list([imports])
        for import_ in imports:
            if not import_ in _ejectables:
                _ejectables[import_] = {
                    "base": None, "deps": [], "globals": [], "sources": [],
                    "imports": import_
                }

    if alias:
        key, value = alias["key"], alias["alias"]
        if not key in _ejectables:
            _ejectables[key] = { "name": key,
                "imports": [alias["imports"]], "alias": value, "base": None, "deps": [], "globals": [], "sources": []
            }

    def decorator(fn, deps = deps, globals_ = globals_):
        name = _get_name(fn)
        if not name in _ejectables:
            _ejectables[name] = {
                "base": None, "deps": [], "globals": [], "sources": [],
                "imports": imports
            }

        _ejectables[name]["base"] = fn
        
        if deps:
            deps = deps if isinstance(deps, (list, tuple)) else list([deps])
            for dep in deps:
                _ejectables[name]["deps"].append(dep)
        
        if globals_:
            for key, glob in globals_.items():
                value = globals_[key]
                _ejectables[name]["globals"].append({
                    "key": key, "value": value
                })

        if sources:
            for source in list(sources):
                source = upy.import_handler(source)
                _ejectables[name]["sources"].append(source)

        import inspect

        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return fn if inspect.isclass(fn) else wrapper

    return decorator