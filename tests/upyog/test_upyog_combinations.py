def test_upyog_combinations():
    import upyog as upy

    assert upy.combinations({
        "foo": [None, [], ["1", "2"]],
        "bar": [None, [], ["a", "b"]],
    }) == [
        {"foo": None, "bar": None},
        {"foo": None, "bar": []},
        {"foo": None, "bar": ["a", "b"]},
        {"foo": [], "bar": None},
        {"foo": [], "bar": []},
        {"foo": [], "bar": ["a", "b"]},
        {"foo": ["1", "2"], "bar": None},
        {"foo": ["1", "2"], "bar": []},
        {"foo": ["1", "2"], "bar": ["a", "b"]},
    ]