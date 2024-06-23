# imports - standard imports
import os

# imports - module imports
from upyog.util.types 	import auto_typecast
from upyog._compat		import string_types
from upyog.util.eject import ejectable
from upyog.util.array import is_list_like
from upyog.util._dict import dict_from_list
from upyog._compat import iteritems
from upyog.util.types import lmap

@ejectable()
def getenvvar(name, prefix = None, seperator = "_"):
    """
        Get the environment variable name.

        Args:
            name (str): The name of the environment variable.
            prefix (str): Prefix for the environment variable.
            seperator (str): Seperator for the environment variable.

        Returns:
            str: The environment variable name.

        Example:
            >>> getenvvar("HOME")
            'HOME'
            >>> getenvvar("HOME", prefix = "JOBS")
            'JOBS_HOME'
            >>> getenvvar("HOME", prefix = "JOBS", seperator = "_A_")
            'JOBS_A_HOME'
    """
    if not prefix:
        prefix	  = ""
        seperator = ""

    envvar = "%s%s%s" % (prefix, seperator, name)
    return envvar

@ejectable(deps = ["dict_from_list", "getenvvar", "auto_typecast"])
def getenv(name, default = None, cast = True, prefix = None, seperator = "_", raise_err = False):
    """
        Get an environment variable.

        Args:
            name (str): The name of the environment variable.
            default (str): Default value if the environment variable is not found.
            cast (bool): Automatically typecast the value.
            prefix (str): Prefix for the environment variable.
            seperator (str): Seperator for the environment variable.
            raise_err (bool): Raise an error if the environment variable is not found.

        Returns:
            str: The value of the environment variable.

        Example:
            >>> getenv("HOME")
            '/home/user'
            >>> getenv("HOME", default = "/home/user")
            '/home/user'
            >>> getenv("HOME", default = "/home/user", cast = False)
            '/home/user'
            >>> os.environ["PI"] = "3.14"
            >>> getenv("PI", default = 3.14, cast = True)
            3.14
            >>> os.environ["FOO_BAR"] = "baz"
            >>> getenv("FOO", default = "baz", prefix = "BAR")
            'baz'
    """
    import os

    envvar = getenvvar(name, prefix = prefix, seperator = seperator)

    if not envvar in dict_from_list(os.environ) and raise_err:
        raise KeyError("Environment Variable %s not found." % envvar)

    value  = os.getenv(envvar, default)
    value  = auto_typecast(value) if cast else value

    return value

def setenv(name, value, overwrite = False, prefix = None, seperator = "_", raise_err = False):
    envvar = getenvvar(name, prefix = prefix, seperator = seperator)
    set_   = False
    
    if envvar in list(os.environ):
        if overwrite:
            set_ = True
        else:
            if raise_err:
                raise ValueError("Environment Variable %s already set." % envvar)
    else:
        set_ = True

    if set_:
        os.environ[envvar] = value

@ejectable()
def value_to_envval(value):
    """
    Convert python types to environment values
    """

    if not isinstance(value, string_types):
        if isinstance(value, bool):
            if value == True:
                value = "true"
            elif value == False:
                value = "false"
        elif isinstance(value, (int, float)):
            value = str(value)
        else:
            raise TypeError("Unknown parameter type %s with value %r" % (value, type(value)))

    return value

SECRETS = (
    getenvvar("JOBS_GITHUB_TOKEN"),
)

@ejectable(deps = ["iteritems", "is_list_like", "value_to_envval", "lmap"])
def create_param_string(**kwargs):
    string = ""

    for i, (key, value) in enumerate(iteritems(kwargs)):
        if is_list_like(value):
            value = ",".join(lmap(str, value))
        else:
            value = value_to_envval(value)

        string += "%s=%s" % (key, value)

        if i < len(kwargs) - 1:
            string += ";"

    return string