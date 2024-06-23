from math import *

from upyog.util.array import is_list_like

def sign(x):
    """
    Get the sign of a number.

    :param x: The number to get the sign of.

    Example::

        sign(1)
        1
        sign(-1)
        -1
    """
    return (1, -1)[x < 0]

def avg(*args):
    """
    Get the average of a list of numbers.

    :param args: The numbers to get the average of.

    Example::

        avg(1, 2, 3)
        2.0
    """
    if is_list_like(args[0]):
        args = args[0]

    if len(args) == 0:
        return 0

    return sum(args) / len(args)

def _div(a, b, raise_err = False):
    try:
        return a / b
    except ZeroDivisionError:
        if raise_err:
            raise
    return nan

def div(a, b):
    """
    Divide two numbers.

    :param a: The numerator.
    :param b: The denominator.

    Example::

        div(1, 2)
        0.5
    """
    if is_list_like(a) and is_list_like(b):
        return [_div(a[i], b[i]) for i in range(len(a))]

    if is_list_like(a):
        return [_div(a[i], b) for i in range(len(a))]
    
    if is_list_like(b):
        return [_div(a, b[i]) for i in range(len(b))]

    return _div(a, b)

def percentile(arr, p):
    """
        Returns the pth percentile of the array.
    """
    length  = len(arr)
    sorted_ = sorted(arr)

    if not arr:
        return nan

    return sorted_[int(ceil((length * p) / 100 )) - 1]

def lt(a, b):
    return a < b

def gt(a, b):
    return a > b