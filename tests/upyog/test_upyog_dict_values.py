def test_upyog_dict_values():
    import pytest
    import upyog as upy

    assert list(upy.dict_values({})) == []
    assert list(upy.dict_values({ "foo": 1, "bar": 2 })) == [1, 2]

    with pytest.raises(AttributeError):
        upy.dict_values([1, 2, 3])