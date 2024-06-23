def test_upyog_getenv():
    import os

    import pytest
    import unittest.mock as mock
    
    import upyog as upy

    with mock.patch.dict(os.environ, { "FOO": "bar" }, clear = True):
        assert upy.getenv("FOO") == "bar"

    with mock.patch.dict(os.environ, { "PI": "3.14" }, clear = True):
        assert upy.getenv("PI") == 3.14

    with mock.patch.dict(os.environ, { "FOO_A_BAR": "baz" }, clear = True):
        assert upy.getenv("BAR", prefix = "FOO", seperator = "_A_") == "baz"

    assert upy.getenv("FOO", default = "bar") == "bar"

    with pytest.raises(KeyError):
        upy.getenv("FOO", raise_err = True)
