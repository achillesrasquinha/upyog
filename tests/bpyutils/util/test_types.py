# imports - module imports
from bpyutils.util.types import (
    get_function_arguments,
    lfilter,
    lmap,
    build_fn
)

def test_get_function_arguments():
    def foobar(foo = "bar", bar = "baz"):
        pass
    def barfoo():
        pass
    foobar(); barfoo() # Increase coverage
    
    assert get_function_arguments(foobar) == dict(foo = "bar", bar = "baz")
    assert get_function_arguments(barfoo) == dict()

def test_lfilter():
    l = [1, 2, 3, 4, 5]
    is_even = lambda x: x % 2 == 0

    assert lfilter(is_even, l) == list(filter(is_even, l))

def test_lmap():
    l = [1, 2, 3, 4, 5]
    add_5 = lambda x: x + 5

    assert lmap(add_5, l) == list(map(add_5, l))

def test_build_fn():
    def add(a, b):
        return a + b

    fn = build_fn(add, a = 1, b = 2)
    assert fn() == 3

import pytest

from bpyutils.util.types import (
  auto_typecast,
  _gen_to_seq
)

def test_auto_typecast():
	raise NotImplementedError

def test__gen_to_seq():
	raise NotImplementedError