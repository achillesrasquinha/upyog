def test_upyog_merge_dict():
    import upyog as upy

    assert upy.merge_dict({}, {}) == {}
    assert upy.merge_dict({ "foo": "bar" }, {}) == { "foo": "bar" }
    assert upy.merge_dict({}, { "foo": "bar" }) == { "foo": "bar" }

    assert upy.merge_dict({ "foo": "bar" }, { "bar": "baz" }, { "baz": "boo" }) == { "foo": "bar", "bar": "baz", "baz": "boo" }
    assert upy.merge_dict({ "foo": "bar" }, { "foo": "baz", "bar": "boo" })     == { "foo": "baz", "bar": "boo" }

    assert upy.merge_dict({ "foo": "bar" }, { "foo": "baz" }, deep=True) == { "foo": "baz" }
    assert upy.merge_dict({ "foo": { "bar": "baz" } }, { "foo": { "baz": "boo" } }, deep=True) == { "foo": { "bar": "baz", "baz": "boo" } }

    assert upy.merge_dict({ "foo": "bar" }, { "foo": "baz" }, { "foo": "boo" }, deep=True)     == { "foo": "boo" }