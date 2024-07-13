def test_upyog_sequencify():
    import upyog as upy
    
    assert upy.sequencify("foobar") == ["foobar"]
    assert upy.sequencify([1,2,3])  == [1,2,3]
    assert upy.sequencify([1,2,3])  != [3,2,1]
    assert upy.sequencify([])       == []
    assert upy.sequencify(None)     == [None]

    assert upy.sequencify("foobar", type_ = tuple) == ("foobar",)
    assert upy.sequencify([1,2,3],  type_ = tuple) == (1,2,3)
    assert upy.sequencify([1,2,3],  type_ = tuple) != (3,2,1)
    assert upy.sequencify([],       type_ = tuple) == tuple()
    assert upy.sequencify(None,     type_ = tuple) == (None,)