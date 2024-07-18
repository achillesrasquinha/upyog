def test_upyog_import_or_raise():
    import pytest
    import upyog as upy

    assert upy.import_or_raise("pytest") == pytest

    with pytest.raises(ImportError):
        upy.import_or_raise("tensorflow")