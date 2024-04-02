from upyog._compat import iteritems
from upyog.util.eject import ejectable

@ejectable()
def to_css_str(style):
    """
    Convert a dictionary of CSS style to a string.

    Args:
    - style: dict

    Returns:
    - str
    """
    return ";".join([f"{k}:{v}" for k, v in iteritems(style)])