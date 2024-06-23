def test_upyog_lower():
    import upyog as upy

    assert upy.lower("HELLO")        == "hello"
    assert upy.lower("HELLO WORLD")  == "hello world"
    assert upy.lower("HELLO WORLD!") == "hello world!"
    assert upy.lower("hello")        == "hello"
    assert upy.lower("hElLo")        == "hello"