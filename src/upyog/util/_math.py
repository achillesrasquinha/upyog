from math import *

from upyog.util.array import is_list_like

def sign(x):
    """
    Get the sign of a number.

    :param x: The number to get the sign of.

    Example::

        >>> upy.sign(1)
        1
        >>> upy.sign(-1)
        -1
    """
    return (1, -1)[x < 0]

def avg(*args):
    """
    Get the average of a list of numbers.

    :param args: The numbers to get the average of.

    Example::

        >>> upy.avg(1, 2, 3)
        2.0
    """
    if is_list_like(args[0]):
        args = args[0]

    if len(args) == 0:
        return 0

    return sum(args) / len(args)

def div(a, b):
    """
    Divide two numbers.

    :param a: The numerator.
    :param b: The denominator.

    Example::

        >>> upy.div(1, 2)
        0.5
    """
    if is_list_like(a) and is_list_like(b):
        return [a[i] / b[i] for i in range(len(a))]

    if is_list_like(a):
        return [a[i] / b for i in range(len(a))]
    
    if is_list_like(b):
        return [a / b[i] for i in range(len(b))]

    return a / b

def percentile(arr, p):
    """
        Returns the pth percentile of the array.
    """
    length  = len(arr)
    sorted_ = sorted(arr)

    return sorted_[int(ceil((length * p) / 100 )) - 1]

def lt(a, b):
    return a < b

def gt(a, b):
    return a > b