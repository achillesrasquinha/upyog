def test_upyog_format_ansi():
    import pytest
    import upyog as upy

    assert upy.format_ansi("0;30") == "\033[0;30m"
    assert upy.format_ansi("0;31") == "\033[0;31m"
    assert upy.format_ansi("0;32") == "\033[0;32m"

    with pytest.raises(ValueError):
        upy.format_ansi("foo")