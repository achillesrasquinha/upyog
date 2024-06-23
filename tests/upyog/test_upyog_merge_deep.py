def test_upyog_merge_deep():
    import upyog as upy

    assert upy.merge_deep({ "foo": "bar" }, { "foo": "baz" }) == { "foo": "baz" }
    assert upy.merge_deep({ "foo": { "bar": "baz" } }, { "foo": { "baz": "boo" } }) == { "foo": { "bar": "baz", "baz": "boo" } }