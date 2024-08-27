def test_read(tmpdir):
    import upyog as upy

    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("foobar.txt")
    tempfile.write("foobar")

    assert tempfile.read() == upy.read(tempfile)
    assert tempfile.read() == upy.read(str(tempfile))

    tempfile  = directory.join("barfoo.txt")
    tempfile.write(\
        """
        foobar
        \n
        barfoo
        """
    )

    content = tempfile.read()
    assert upy.strip(content) == upy.read(str(tempfile))
    assert content == upy.read(str(tempfile), clean = False)