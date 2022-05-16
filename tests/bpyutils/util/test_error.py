import pytest

from bpyutils.util.error import pretty_print_error

def test_pretty_print_error():
    try:
        raise TypeError("This is a type error.")
    except TypeError as e:
        pretty_print_error(e)