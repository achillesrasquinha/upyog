# imports - module imports
from upyog.util._dict import (
    dict_from_list
)

def test_dict_from_list():
    assert dict_from_list(["foo", "bar"], [1, 2]) == dict(foo = 1, bar = 2)
    assert dict_from_list([1, 2], ["foo", "bar"]) == { 1: "foo", 2: "bar" }

import pytest

from upyog.util._dict import (
  merge_deep,
  AutoDict,
  autodict
)

def test_merge_deep():
	raise NotImplementedError

def test_auto_dict():
	raise NotImplementedError

def test_autodict():
	raise NotImplementedError



