# imports - compatibility imports
from __future__ import print_function, absolute_import

from upyog._compat import input

# imports - standard imports
import sys, os
import platform
import inspect

# imports - module imports
from upyog._compat         import EX_OK
from upyog.util.system     import write
from upyog.util.string     import strip_ansi
from upyog.util.environ    import getenv
from upyog.util.eject      import ejectable
from upyog.util.cli        import can_ansi_format, can_ansi_format_windows

_ACCEPTABLE_INPUTS_YES      = ("", "y", "Y")
_ACCEPTABLE_INPUTS_QUIT     = ("q", "Q")

_ANSI_FORMAT = "\033[{}m"
_format_ansi = lambda x: _ANSI_FORMAT.format(x)

BOLD      = _format_ansi("0;1")
GRAY      = _format_ansi("0;90")
RED       = _format_ansi("0;91")
GREEN     = _format_ansi("0;92")
YELLOW    = _format_ansi("0;93")
CYAN      = _format_ansi("0;96")
ORANGE    = _format_ansi("0;40")
CLEAR     = _format_ansi("0")

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

def add_github_args(parser, env_prefix = None):
    parser.add_argument("--github-access-token",
        help    = "GitHub Access Token",
        default = getenv("GITHUB_ACCESS_TOKEN", prefix = env_prefix)
    )
    parser.add_argument("--github-reponame",
        help    = "GitHub Repository Name",
        default = getenv("GITHUB_REPONAME", prefix = env_prefix)
    )
    parser.add_argument("--github-username",
        help    = "GitHub Username",
        default = getenv("GITHUB_USERNAME", prefix = env_prefix)
    )
    return parser

def format(string, type_):
    import sys

    if can_ansi_format_windows(): # pragma: no cover
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    if can_ansi_format() or "pytest" in sys.modules:
        string = "{}{}{}".format(type_, string, CLEAR)

    return string