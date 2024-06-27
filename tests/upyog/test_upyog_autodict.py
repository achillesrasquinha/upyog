def test_upyog_autodict():
    import pytest
    import upyog as upy

    assert upy.autodict()   == {}
    assert upy.autodict({}) == {}

    assert upy.autodict({'a': 1}) == {'a': 1}

    d = upy.autodict({ 'a': 1, 'b': 2, 'c': 3 })
    assert d == {'a': 1, 'b': 2, 'c': 3}
    
    d["d"]["e"]["f"] = 4
    assert d == {'a': 1, 'b': 2, 'c': 3, 'd': {'e': {'f': 4}}}

    with pytest.raises(TypeError):
        upy.autodict(1)

    assert repr(upy.autodict())         == repr({})
    assert repr(upy.autodict({"a": 1})) == repr({"a": 1})