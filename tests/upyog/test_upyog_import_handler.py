def test_upyog_import_handler():
    import pytest
    import upyog as upy

    assert upy.import_handler("pytest") == pytest

    from os.path import abspath
    assert upy.import_handler("os.path.abspath") == abspath

    with pytest.raises(ImportError):
        upy.import_handler("tensorflow")