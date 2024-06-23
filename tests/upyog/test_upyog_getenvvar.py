def test_upyog_getenvvar():
    import upyog as upy

    assert upy.getenvvar("HOME") == "HOME"
    assert upy.getenvvar("BAR", prefix = "FOO") == "FOO_BAR"
    assert upy.getenvvar("BAR", prefix = "FOO", seperator = "_A_") == "FOO_A_BAR"