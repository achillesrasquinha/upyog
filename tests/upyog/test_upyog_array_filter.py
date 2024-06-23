def test_upyog_array_filter():
    import upyog as upy

    assert upy.array_filter(lambda x: x > 2, [1, 2, 3, 4, 5]) == [3, 4, 5]

    a, b, = upy.array_filter(lambda x: x > 2, [1, 2, 3, 4, 5], other = True)
    assert a == [3, 4, 5]
    assert b == [1, 2]

    assert upy.array_filter([1, 3, 5], [1, 2, 3, 4, 5])  == [2, 4]
    assert upy.array_filter(None, [1, None, 3, None, 5]) == [1, 3, 5]