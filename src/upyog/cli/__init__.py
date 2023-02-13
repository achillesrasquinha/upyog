from __future__ import absolute_import

# imports - module imports
from upyog.cli.util   import *
from upyog.cli.parser import get_args
from upyog.util._dict import merge_dict
from upyog.util.types import get_function_arguments

def create_command(args_getter):

    def fn(*fn_args, **fn_kwargs):
        args    = args_getter()
        
        params  = get_function_arguments(fn)

        params  = merge_dict(params, args)
        
        def wrapper(*args, **kwargs):
            return fn(**params)
        
        return wrapper
    return fn

command = create_command(get_args)