def test_upyog_str2bool():
    import upyog as upy
    import pytest

    assert upy.str2bool("True")  == True
    assert upy.str2bool("true")  == True

    assert upy.str2bool("False") == False
    assert upy.str2bool("false") == False

    assert upy.str2bool("None")  == None
    assert upy.str2bool("null")  == None
    assert upy.str2bool("NULL")  == None

    with pytest.raises(ValueError):
        upy.str2bool("foo", raise_err = True)

    assert not upy.str2bool("foo", raise_err = False)