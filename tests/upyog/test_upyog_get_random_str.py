def test_upyog_get_random_str():
    import upyog as upy

    assert upy.get_random_str()
    assert len(upy.get_random_str()) == 32
    assert len(upy.get_random_str(remove_hyphens = False)) == 36
    assert len(upy.get_random_str(16)) == 16

    assert upy.get_random_str() != upy.get_random_str()