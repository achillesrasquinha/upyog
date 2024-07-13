def test_upyog_noop():
    import upyog as upy

    assert upy.noop()  == None
    assert upy.noop(1) == None