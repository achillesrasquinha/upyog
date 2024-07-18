def test_upyog_squash():
    import upyog as upy

    assert upy.squash(["foo"])          == "foo"
    assert upy.squash(["foo", "bar"])   == ["foo", "bar"]

    assert upy.squash([["foo"]])        == ["foo"]
    assert upy.squash([["foo", "bar"]]) == ["foo", "bar"]

    assert upy.squash((1,))             == 1
    assert upy.squash((1, 2))           == (1, 2)