from __future__ import absolute_import

# imports - standard imports
import os, sys
import argparse
import multiprocessing as mp
import json

# imports - module imports
from upyog.__attr__     import (
    __name__,
    __version__,
    __description__,
    __command__,
    __author__,
    __email__
)
from upyog.i18n import _
from upyog.util.environ    import getenv
from upyog.cli             import util as _cli
from upyog.cli.formatter   import ArgumentParserFormatter
from upyog.cli.util        import _CAN_ANSI_FORMAT, add_github_args
from upyog.util.git        import resolve_git_url
from upyog.util.system     import check_file
from upyog.config          import load_config

_DESCRIPTION_JUMBOTRON = \
"""
%s (v %s)

%s
""" % (
    _cli.format(__name__,        _cli.RED),
    _cli.format(__version__,     _cli.BOLD),
    _cli.format(__description__, _cli.BOLD)
)

class ConfigFileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string = None):
        config = load_config(values)
        setattr(namespace, self.dest, config)

def get_base_parser(prog, description, help_ = True):
    parser = argparse.ArgumentParser(
        prog            = prog,
        description     = description,
        add_help        = False,
        formatter_class = ArgumentParserFormatter
    )
    parser.add_argument("--cwd",
        default = getenv("CWD", os.getcwd()),
        help    = "Current Working Directory."
    )
    parser.add_argument("-y", "--yes",
        action  = "store_true",
        default = getenv("ACCEPT_ALL_DIALOGS", False),
        help    = "Confirm for all dialogs."
    )
    parser.add_argument("-c", "--check",
        action  = "store_true",
        default = getenv("DRY_RUN", False),
        help    = "Perform a dry-run."
    )
    parser.add_argument("-i", "--interactive",
        action  = "store_true",
        default = getenv("INTERACTIVE", False),
        help    = "Interactive Mode."
    )
    parser.add_argument("-j", "--jobs",
        type    = int,
        help    = "Number of Jobs to be used.",
        default = getenv("JOBS", max(mp.cpu_count(), 4))
    )
    parser.add_argument("-o", "--output",
        default = getenv("OUTPUT_FILE"),
        help    = "Print Output to File."
    )
    parser.add_argument("--config",
        default = getenv("CONFIG_FILE"),
        help    = "Configuration File.",
        type    = check_file,
        action  = ConfigFileAction
    )
    parser.add_argument("--input",
        default = getenv("INPUT_FILE"),
        help    = "Input File."
    )
    parser.add_argument("--ignore-error",
        action  = "store_true",
        default = getenv("IGNORE_ERROR", False),
        help    = "Ignore Error in case of failure."
    )
    parser.add_argument("--force",
        action  = "store_true",
        default = getenv("FORCE", False),
        help    = "Force."
    )

    if _CAN_ANSI_FORMAT or "pytest" in sys.modules:
        parser.add_argument("--no-color",
            action  = "store_true",
            default = getenv("NO_COLOR", False),
            help    = "Avoid colored output."
        )

    parser.add_argument("-V", "--verbose",
        action  = "store_true",
        help    = "Display verbose output.",
        default = getenv("VERBOSE", False)
    )
    parser.add_argument("-v", "--version",
        action  = "version",
        version = __version__,
        help    = "Show %s's version number and exit." % __name__
    )

    if help_:
        parser.add_argument("-h", "--help",
            action  = "help",
            default = argparse.SUPPRESS,
            help    = "Show this help message and exit."
        )

    return parser

def get_parser():
    parser = get_base_parser(__command__, _DESCRIPTION_JUMBOTRON,
        help_ = False)

    # boilpy

    parser.add_argument("--update-boilpy-project",
        type    = resolve_git_url,
        help    = _("Update project")
    )
    parser.add_argument("--project-branch",
        help    = "Project branch to checkout from"
    )
    parser.add_argument("--overwrite-project",
        action  = "store_true",
        help    = "Overwrite changes within project"
    )
    parser.add_argument("--boilpy-path",
        type    = resolve_git_url,
        help    = "Path to BoilPy repostitory",
        default = "https://github.com/achillesrasquinha/boilpy"
    )

    parser = add_github_args(parser, env_prefix = __name__.replace("-", "_").upper())

    parser.add_argument("--run-job",
        action  = "append",
        help    = "Run a specific job"
    )
    parser.add_argument("--run-jobs",
        action  = "append",
        help    = "Run all jobs"
    )
    parser.add_argument("-m", "--method",
        action  = "append",
        help    = "Run Method"
    )
    parser.add_argument("--run-ml",
        help    = "Run ML pipeline"
    )
    parser.add_argument("--online",
        action  = "store_true",
        help    = "Run ML pipeline in online mode"
    )
    parser.add_argument("-p", "--param",
        action  = "append",
        help    = "Parameters"
    )
    parser.add_argument("--dbshell",
        default = getenv("DATABASE_SHELL"),
        help    = "Activate database shell."
    )

    parser.add_argument("--generate-tests",
        help    = "generate test cases for a package"
    )
    parser.add_argument("--generate-docs",
        help    = "generate doc strings for a package"
    )
    parser.add_argument("--generate-translations",
        help    = "generate translations for a package"
    )
    parser.add_argument("--output-dir",
        help    = "output directory for generator"
    )
    parser.add_argument("--git-username",
        help    = "Git Username",
        default = getenv("GIT_USERNAME", __author__)
    )
    parser.add_argument("--git-email",
        help    = "Git Email",
        default = getenv("GIT_EMAIL", __email__)
    )
    parser.add_argument("--no-pretty-error", 
        action  = "store_true",
        default = getenv("NO_PRETTY_ERROR", False),
        help    = "Disable Pretty Error"
    )

    if any("upyog" in arg for arg in sys.argv):
        parser.add_argument("-h", "--help",
            action  = "help",
            default = argparse.SUPPRESS,
            help    = "Show this help message and exit."
        )

    return parser

def get_parser_args(parser, args = None, known = True, as_dict = True):
    if known:
        args, _ = parser.parse_known_args(args)
    else:
        args    = parser.parse_args(args)

    if as_dict:
        args = args.__dict__
        
    return args

def get_args(args = None, known = True, as_dict = True):
    parser = get_parser()
    return get_parser_args(parser, args = args, known = known, as_dict = as_dict)

def _render_jumbotron(name, version = None, description = None):
    jumbotron = \
"""
%s (v %s)

%s
""" % (
    _cli.format(__name__,        _cli.RED),
    _cli.format(__version__,     _cli.BOLD),
    _cli.format(__description__, _cli.BOLD)
)

    return jumbotron