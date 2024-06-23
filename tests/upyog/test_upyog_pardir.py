def test_upyog_pardir():
    import os, os.path as osp
    
    import pytest

    import upyog as upy

    cwd = osp.abspath(os.getcwd())

    assert upy.pardir("foo/bar/baz",    raise_err = False) == osp.join(cwd, "foo/bar")
    assert upy.pardir("foo/bar/baz", 2, raise_err = False) == osp.join(cwd, "foo")
    assert upy.pardir("foo/bar/baz", 3, raise_err = False) == cwd
    assert upy.pardir("foo/bar/baz", 4, raise_err = False) == osp.dirname(cwd)

    assert upy.pardir("/",           9, raise_err = False) == "/"

    with pytest.raises(FileNotFoundError):
        upy.pardir("foo/bar/baz")

    with pytest.raises(ValueError):
        upy.pardir("/", 9) # level is too high

    assert upy.pardir(__file__) == osp.join(cwd, osp.dirname(__file__))