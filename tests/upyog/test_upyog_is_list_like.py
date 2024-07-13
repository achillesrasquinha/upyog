def test_upyog_is_list_like():
    import upyog as upy

    assert upy.is_list_like([1, 2, 3]) == True
    assert upy.is_list_like((1, 2, 3)) == True
    assert upy.is_list_like({1, 2, 3}) == True
    assert upy.is_list_like(frozenset([1, 2, 3])) == True

    assert not upy.is_list_like(1)
    assert not upy.is_list_like('a')