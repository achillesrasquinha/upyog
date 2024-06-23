def test_upyog_get_ansi_code():
    import pytest
    import upyog as upy

    assert upy.get_ansi_code("red")    == "\033[0;91m"
    assert upy.get_ansi_code("green")  == "\033[0;92m"
    assert upy.get_ansi_code("yellow") == "\033[0;93m"

    with pytest.raises(ValueError):
        upy.get_ansi_code("foo")