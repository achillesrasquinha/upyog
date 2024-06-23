def test_upyog_dict_items():
    import pytest

    import upyog as upy

    assert list(upy.dict_items({})) == []
    assert list(upy.dict_items({ "foo": 1, "bar": 2 })) == [("foo", 1), ("bar", 2)]

    with pytest.raises(AttributeError):
        upy.dict_items([1, 2, 3])