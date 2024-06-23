def test_upyog_check_array():
    import pytest

    import upyog as upy

    assert upy.check_array([1, 2, 3]) == True
    assert upy.check_array((1, 2, 3)) == True
    assert upy.check_array({1, 2, 3}) == True

    assert upy.check_array("foo", raise_err = False) == False

    with pytest.raises(TypeError):
        upy.check_array("foo")

