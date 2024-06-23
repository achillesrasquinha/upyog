def test_upyog_auto_typecast():
    import upyog as upy

    assert upy.auto_typecast("True")  == True
    assert upy.auto_typecast("true")  == True

    assert upy.auto_typecast("False") == False
    assert upy.auto_typecast("false") == False

    assert upy.auto_typecast("None")  == None
    assert upy.auto_typecast("null")  == None
    assert upy.auto_typecast("NULL")  == None

    assert upy.auto_typecast("1.2345")  == 1.2345
    assert upy.auto_typecast("12345")   == 12345
    assert upy.auto_typecast("12345.0") == 12345

    from datetime import datetime as dt
    assert upy.auto_typecast("2018-01-01")          == dt(2018, 1, 1)
    assert upy.auto_typecast("2018-01-01 00:00:00") == dt(2018, 1, 1, 0, 0, 0)




