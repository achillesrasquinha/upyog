def test_upyog_get_log_level():
    import pytest
    import logging
    import upyog as upy

    levels = ("NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    for level in levels:
        assert upy.get_log_level(level) == getattr(logging, level)

    assert upy.get_log_level("SUCCESS") == 21
    assert upy.get_log_level("MAGIC")   == 22

    with pytest.raises(ValueError):
        upy.get_log_level("foobar")