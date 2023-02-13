from __future__ import absolute_import

# imports - module imports
from upyog.cli.util   import *
from upyog.cli.parser import get_parser
from upyog.util._dict import merge_dict
from upyog.util.error import pretty_print_error

def create_command(parser):
    def command(*cmd_args, **cmd_kwargs):
        parser_args = vars(parser.parse_args())

        def wrapper(*wrp_args, **wrp_kwargs):
            cmd = wrp_args[0]

            try:
                output = cmd(**parser_args)
            except Exception as e:
                pretty_print_error(e)
                raise e

        return wrapper

    return command

parser  = get_parser()
command = create_command(parser)