def test_upyog_write(tmpdir):
    import os.path as osp

    import upyog as upy

    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("foobar.txt")

    content   = "foobar"
    upy.write(tempfile, content)

    assert content == tempfile.read()

    other     = "barfoo"
    upy.write(tempfile, other, append = True)

    assert content + other == tempfile.read()

    barfoo    = osp.join(str(directory), "barfoo.txt")
    upy.write(barfoo, content, force = True)

    assert content == upy.read(barfoo)
