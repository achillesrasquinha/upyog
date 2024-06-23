def test_upyog_dict_from_list():
    import upyog as upy

    assert upy.dict_from_list(["a", 1, "b", 2]) == {
        "a": None, 1: None, "b": None, 2: None
    }
    assert upy.dict_from_list(["a", "b", "c"], [1, 2, 3]) == {"a": 1, "b": 2, "c": 3}

    assert upy.dict_from_list(["a", "b", "c"]) == {"a": None, "b": None, "c": None}

    assert upy.dict_from_list(["a", "b", "c"], 1) == {"a": 1, "b": 1, "c": 1}

    assert upy.dict_from_list([{"name": "foo"}, {"name": "bar"}], "name") == {"foo": {"name": "foo"}, "bar": {"name": "bar"}}