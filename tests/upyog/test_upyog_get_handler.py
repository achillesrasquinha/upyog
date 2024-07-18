def test_upyog_get_handler():
    import pytest
    import upyog as upy

    assert upy.get_handler("pytest") == pytest

    from os.path import abspath
    assert upy.get_handler("os.path.abspath") == abspath

    with pytest.raises(ImportError):
        upy.get_handler("tensorflow")