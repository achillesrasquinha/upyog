def test_upyog_getattr2():
    import upyog as upy

    d = {
        "a": {
            "b": {
                "c": 1
            }
        }
    }

    assert upy.getattr2(d, "a.b.c") == 1
    assert upy.getattr2(d, "a.b.d") == None

    assert upy.getattr2(d, "a.b.c", 2) == 1
    assert upy.getattr2(d, "a.b.d", 2) == 2

    assert upy.getattr2(d, "a.b.c.d.e.f") == None
    assert upy.getattr2(d, "a.b.c.d.e.f", 2) == 2