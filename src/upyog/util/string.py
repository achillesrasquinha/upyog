# imports - standard imports
import re
import uuid

from upyog._compat import urlparse
from upyog.util.array import sequencify

_REGEX_ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
_REGEX_HTML        = re.compile("<.*?>")

def strip(string, type_ = " \n"):
    string = string.lstrip(type_)
    string = string.rstrip(type_)

    return string

def strip_ansi(string):
    string = _REGEX_ANSI_ESCAPE.sub("", string)
    return string

def pluralize(string, count = 1):
    # A very shitty pluralizer
    if not string.endswith("s"):
        if count > 1:
            string += "s"
    
    return string

def labelize(string):
    result   = ""
    upperize = False

    if string.isupper():
        string = string.lower()

    for i, char in enumerate(string):
        if char.isupper() and i > 0:
            result += " "
        elif char == "_":
            result  += " "
            upperize = True
            continue

        if upperize:
            char = char.upper()
            upperize = False

        result += char

    return result.title()

def kebab_case(string, delimiter = " ", to_lower = True):
    words = string.replace(delimiter, " ").split()
    kebab = "-".join([word.lower() if to_lower else word for word in words])
    
    return kebab

def safe_encode(obj, encoding = "utf-8"):
    try:
        obj = obj.encode(encoding)
    except (AttributeError, UnicodeEncodeError):
        pass
    
    return obj

def safe_decode(obj, encoding = "utf-8"):
    try:
        obj = obj.decode(encoding)
    except (AttributeError, UnicodeDecodeError):
        pass
    
    return obj

def sanitize_html(html):
    sanitized = re.sub(_REGEX_HTML, "", html)
    return sanitized

def sanitize_text(text):
    text = text.replace("&nbsp;", " ")
    text = strip(text)
    return text

def upper(text):
    text = text.upper()
    return text

def lower(text, only = None):
    text = text.lower()
    return text

def capitalize(text):
    text = text.capitalize()
    return text

def ellipsis(string, threshold = 50, pattern = "..."):
    length      = len(string)
    expected    = threshold + len(pattern) 

    if length > expected:
        string = string[:expected]
        string = "%s%s" % (string, pattern)

    return string

def get_random_str(length = None, remove_hyphen = True):
    uuid_   = uuid.uuid4()
    string  = str(uuid_)

    if remove_hyphen:
        string  = string.replace("-", "")

    if length:
        string = string[:length]

    return string

def check_url(s, raise_err = True):
    is_url = False
    
    try:
        result = urlparse(s)
        is_url = all([result.scheme, result.netloc])
    except:
        pass
    
    if not is_url and raise_err:
        raise ValueError("Invalid URL: %s" % s)

    return is_url

def nl(s = "", space = 1):
    space = "\n" * space
    return "%s%s" % (s, space)

def tb(s = "", point = 2, type_ = " "):
    indent = type_ * point
    return "%s%s" % (indent, s)