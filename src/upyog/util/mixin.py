from upyog.model.base  import BaseObject
from upyog.util.string import lower
from upyog._compat     import iteritems

def create_obj(obj_name, base_obj = None, **kwargs):
    base_obj = base_obj or BaseObject

    class CustomObject(base_obj):
        pass

    for key, value in iteritems(kwargs):
        if any([
            key.startswith("fn_"),
            key.startswith("prop_")
        ]):
            name = key.split("_", 1)[1]
            setattr(CustomObject, name, value)

    CustomObject.__name__ = obj_name

    return CustomObject

def create_obj_registerer(registry,
    creator  = None,
    base_obj = None
):
    creator  = creator  or create_obj
    base_obj = base_obj or BaseObject
    
    def register_obj(obj_name, reg_key = None, instance = False, **kwargs):
        CustomObject = creator(
            obj_name = obj_name,
            base_obj = base_obj,
            **kwargs
        )

        if reg_key is None:
            reg_key = lower(CustomObject.__name__)
        
        registry[reg_key] = {
            "class": CustomObject,
        }
        
        return CustomObject

    return register_obj