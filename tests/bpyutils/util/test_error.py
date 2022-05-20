import pytest

from bpyutils.util.error import pretty_print_error

def test_pretty_print_error():
    try:
        raise TypeError("This is a type error.")
    except TypeError as e:
        pretty_print_error(e)

from bpyutils.util.error import (
  _extract_and_format_snippet,
  _get_error_line_info
)

def test__extract_and_format_snippet():
	raise NotImplementedError

def test__get_error_line_info():
	raise NotImplementedError



