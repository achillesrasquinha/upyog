def test_upyog_check_file(tmpdir):
    import pytest
    import upyog as upy

    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("foobar.txt")
    tempfile.write("foobar")

    dirpath   = str(directory)
    fpath     = str(tempfile)

    assert upy.check_file(fpath) == fpath
    # assert not upy.check_file(dirpath, raise_err = False) # TODO: check if dirs are files?

    with pytest.raises(FileNotFoundError):
        upy.check_file(dirpath)

    with pytest.raises(FileNotFoundError):
        upy.check_file("foo")


