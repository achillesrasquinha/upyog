def test_upyog_gen2seq():
    import upyog as upy

    assert upy.gen2seq(filter)(lambda x: x % 2 == 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == [0, 2, 4, 6, 8]
    assert upy.gen2seq(filter)(lambda x: x > 2, [1, 2, 3, 4, 5]) == [3, 4, 5]

    assert upy.gen2seq(map, type_ = tuple)(lambda x: x % 2 == 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == (True, False, True, False, True, False, True, False, True, False)
    assert upy.gen2seq(map, type_ = tuple)(lambda x: x > 2, [1, 2, 3, 4, 5]) == (False, False, True, True, True)

    assert upy.gen2seq(filter, type_ = set)(lambda x: x % 2 == 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == {0, 2, 4, 6, 8}
    assert upy.gen2seq(filter, type_ = set)(lambda x: x > 2, [1, 2, 3, 4, 5]) == {3, 4, 5}