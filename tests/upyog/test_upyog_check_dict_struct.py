def test_upyog_check_dict_struct():
    import pytest
    import upyog as upy

    assert upy.check_dict_struct({}, {}) == {}
    assert upy.check_dict_struct({"a": 1}, {"a": int})
    assert upy.check_dict_struct({"foo": {"bar": 1}}, {"foo": {"bar": int}})

    assert not upy.check_dict_struct({"a": 1}, {"a": str}, raise_err=False)
    assert not upy.check_dict_struct({"a": 1}, {"b": int}, raise_err=False)
    assert not upy.check_dict_struct(
        {"foo": {"bar": {"baz": 1}}}, {"foo": {"bar": {"baz": str}}}, raise_err=False
    )

    with pytest.raises(ValueError):
        upy.check_dict_struct({"foo": {"bar": 1}}, {"foo": {"bar": str}})

    with pytest.raises(ValueError):
        upy.check_dict_struct({"foo": {"bar": {"baz": 1}}}, {"foo": {"bar": {"baz": str}}})

    with pytest.raises(ValueError):
        upy.check_dict_struct({"a": 1}, {"b": int})