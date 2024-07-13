def test_upyog_strip():
    import upyog as upy

    string = "foobar"
    assert upy.strip(string) == string

    string = "\n   foobar\nfoobar   \n   "
    assert upy.strip(string) == "foobar\nfoobar"

    string = "\n\n\n"
    assert upy.strip(string) == ""