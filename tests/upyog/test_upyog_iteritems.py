def test_upyog_iteritems():
    import pytest

    import upyog as upy

    assert list(upy.iteritems({})) == []
    assert list(upy.iteritems({ "foo": 1, "bar": 2 })) == [("foo", 1), ("bar", 2)]

    with pytest.raises(AttributeError):
        upy.iteritems([1, 2, 3])