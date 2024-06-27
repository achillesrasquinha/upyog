import sys
import traceback
import re

from upyog.cli import util as _cli
from upyog.util.string import strip, nl, tb
from upyog.util.types  import lmap
from upyog.util.array  import find
from upyog.util.system import read
from upyog.util.eject  import ejectable
from upyog.util.cli    import cli_format

_REGEX_PATTERN_TEXT_QUOTES = r'"([^"]*)"'
_COLOR_LINE_NUMBER = _cli.GRAY
_INDENT = 4

def _extract_and_format_snippet(path_file, from_ = 0, offset = 3, indent = 4):
    formatted = ""

    try:
        content = read(path_file)
        lines       = content.split("\n")

        lines       = lines[ from_ - offset : from_ + offset ]


        for i, line in enumerate(lines):
            line_num = from_ + i - offset + 1
            line_indent = indent

            line_num_format = ""
            line_num_color  = _COLOR_LINE_NUMBER

            if line_num == from_:
                line_num_format = "%s%s" % (cli_format("→ ", _cli.RED), line_num_format)
                line_indent = 2
                line_num_color = _cli.BOLD

            line_num_format += cli_format(str(line_num), line_num_color) + cli_format("|", _COLOR_LINE_NUMBER)

            formatted_line = nl(tb(line_num_format, line_indent) + tb(line, indent))

            formatted += formatted_line
    except FileNotFoundError:
        pass
            
    return formatted

def _get_error_line_info(error_line):
    strips = lmap(strip, error_line.split("\n"))
    strip_info  = find(strips, lambda x: x.startswith("File"))
    info_strips = lmap(strip, strip_info.split(","))

    info_file, info_line, info_method = info_strips

    re_match = re.search(_REGEX_PATTERN_TEXT_QUOTES, info_file)
    re_group = re_match.group()
    
    path_file = re_group.replace('"', "")
    line_num  = int(info_line[5:])
    method    = info_method[3:]

    return path_file, line_num, method

@ejectable(globals_ = { "_INDENT": _INDENT }, deps = ["nl", "tb"])
def pretty_print_error(e):
    import traceback

    error_type = type(e)
    error_name = error_type.__name__
    error_msg  = getattr(e, "message", str(e))
    indent     = _INDENT
    
    formatted  = nl(tb(cli_format(error_name, _cli.RED), indent))
    if error_msg:
        formatted += nl() + nl(tb(cli_format(error_msg, _cli.BOLD), indent))

    _cli.echo(formatted)

    error_lines = traceback.format_exception(*sys.exc_info())
    error_lines = error_lines[1:-1]

    for error_line in error_lines:
        path_file, line_num, method = _get_error_line_info(error_line)

        formatted = \
            nl(tb("at " + cli_format(path_file, _cli.GREEN)    \
            + cli_format(":%s in " % line_num, _cli.BOLD)      \
            + cli_format(method, _cli.CYAN), indent))

        formatted  += _extract_and_format_snippet(path_file, from_ = line_num,
            indent = 4)
        
        _cli.echo(formatted)