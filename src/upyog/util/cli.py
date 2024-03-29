# imports - compatibility imports
from __future__ import print_function

# imports - standard imports
import sys, os
import platform

# imports - module imports
from upyog._compat         import input, EX_OK

_ACCEPTABLE_INPUTS_YES      = ("", "y", "Y")
_ACCEPTABLE_INPUTS_QUIT     = ("q", "Q")

# https://gist.github.com/RDCH106/6562cc7136b30a5c59628501d87906f7
_CAN_ANSI_FORMAT_WINDOWS    = (
    os.name == "nt" \
        and platform.release() == "10" \
        and platform.version() >= "10.0.14393"
)
_CAN_ANSI_FORMAT            = (
    # check if output is a terminal
    sys.stdout.isatty() \
        # check if stdin and stdout are the same
        or os.fstat(0) == os.fstat(1)
) or _CAN_ANSI_FORMAT_WINDOWS

_ANSI_FORMAT = "\033[{}m"
_format_ansi = lambda x: _ANSI_FORMAT.format(x)

BOLD      = _format_ansi("0;1")
GRAY      = _format_ansi("0;98")
RED       = _format_ansi("0;91")
GREEN     = _format_ansi("0;92")
YELLOW    = _format_ansi("0;93")
CYAN      = _format_ansi("0;96")
ORANGE    = _format_ansi("0;40")
PURPLE    = _format_ansi("0;95")
CLEAR     = _format_ansi("0")

def confirm(query, quit_ = True):
    choices = "[Y/n%s]" % "/q" if quit_ else ""
    query   = "%s %s: " % (query, choices)

    output  = input(query)

    if output in _ACCEPTABLE_INPUTS_QUIT:
        sys.exit(EX_OK)
    
    return output in _ACCEPTABLE_INPUTS_YES

def format(string, type_):
    if _CAN_ANSI_FORMAT_WINDOWS: # pragma: no cover
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    if _CAN_ANSI_FORMAT or "pytest" in sys.modules:
        string = "{}{}{}".format(type_, string, CLEAR)

    return string