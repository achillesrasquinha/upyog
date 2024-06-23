def test_upyog_dict_keys():
    import pytest
    import upyog as upy

    assert list(upy.dict_keys({})) == []
    assert list(upy.dict_keys({ "foo": 1, "bar": 2 })) == ["foo", "bar"]

    with pytest.raises(AttributeError):
        upy.dict_keys([1, 2, 3])