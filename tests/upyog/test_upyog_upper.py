def test_upyog_upper():
    import upyog as upy

    assert upy.upper("hello")        == "HELLO"
    assert upy.upper("hello world")  == "HELLO WORLD"
    assert upy.upper("hello world!") == "HELLO WORLD!"
    assert upy.upper("HELLO")        == "HELLO"
    assert upy.upper("hElLo")        == "HELLO"