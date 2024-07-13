# imports - compatibility imports
from __future__ import print_function, absolute_import

from upyog._compat import input

# imports - standard imports
import sys, os
import platform

# imports - module imports
from upyog.util.string     import strip_ansi, lower
from upyog.util.eject      import ejectable

_ACCEPTABLE_INPUTS_YES      = ("", "y", "Y")
_ACCEPTABLE_INPUTS_QUIT     = ("q", "Q")

def confirm(query, quit_ = True):
    choices = "[Y/n%s]" % "/q" if quit_ else ""
    query   = "%s %s: " % (query, choices)

    output  = input(query)

    if output in _ACCEPTABLE_INPUTS_QUIT:
        sys.exit(EX_OK)
    
    return output in _ACCEPTABLE_INPUTS_YES

def echo(string = "", file = None, nl = True):
    nl = "\n" if nl else ""
    
    print(string, end = nl)
    
    if file:
        string = strip_ansi(string)
        upy.write(file, string + nl, append = True)

@ejectable()
def format_ansi(code):
    """
        Format a string with ANSI escape codes.

        Args:
            code (str): ANSI escape code.

        Returns:
            str: Formatted string.

        Example:
            >>> format_ansi("0;30")
            "\033[0;30m"
            >>> format_ansi("0;31")
            "\033[0;31m"
            >>> format_ansi("0;32")
            "\033[0;32m"
    """
    import re

    pattern   = r"\033\[(\d+;)*\d+m"
    formatted = "\033[%sm" % code

    if not re.match(pattern, formatted):
        raise ValueError("Invalid ANSI escape code: %s" % code)

    return formatted

@ejectable(deps = ["format_ansi", "lower"])
def get_ansi_code(code):
    code = lower(code)

    cmap  = {
        "bold"      : format_ansi("0;1"),
        "gray"      : format_ansi("0;90"),
        "red"       : format_ansi("0;91"),
        "green"     : format_ansi("0;92"),
        "yellow"    : format_ansi("0;93"),
        "cyan"      : format_ansi("0;96"),
        "orange"    : format_ansi("0;40"),
        "clear"     : format_ansi("0"),
        "purple"    : format_ansi("0;95")
    }

    if code not in cmap:
        raise ValueError("Invalid ansi code: %s" % code)

    return cmap[code]

@ejectable()
def can_ansi_format_windows():
    import os, platform

    return (
        os.name == "nt" \
            and platform.release() == "10" \
            and platform.version() >= "10.0.14393"
    )

@ejectable(deps = ["can_ansi_format_windows"])
def can_ansi_format():
    import os, sys

    return (
        # check if output is a terminal
        sys.stdout.isatty() \
            # check if stdin and stdout are the same
            or os.fstat(0) == os.fstat(1)
    ) or can_ansi_format_windows()

@ejectable()
def cli_format(string, type_):
    import sys

    if can_ansi_format_windows(): # pragma: no cover
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    if can_ansi_format() or "pytest" in sys.modules:
        clear  = get_ansi_code("clear")
        string = "{}{}{}".format(type_, string, clear)

    return string