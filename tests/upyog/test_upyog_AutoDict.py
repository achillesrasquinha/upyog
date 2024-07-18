def test_upyog_AutoDict():
    import upyog as upy

    d = upy.AutoDict(int)
    assert d["foo"] == 0