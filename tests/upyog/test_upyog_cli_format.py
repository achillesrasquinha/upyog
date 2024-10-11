def test_upyog_cli_format():
    import upyog as upy
    
    assert upy.cli_format("test", upy.get_ansi_code("bold")) \
        == "\x1b[0;1mtest\x1b[0m"
    assert upy.cli_format("test", upy.get_ansi_code("gray")) \
        == "\x1b[0;90mtest\x1b[0m"
    assert upy.cli_format("test", upy.get_ansi_code("red"))  \
        == "\x1b[0;91mtest\x1b[0m"