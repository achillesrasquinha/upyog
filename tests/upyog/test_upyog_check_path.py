def test_upyog_check_path(tmpdir):
    import pytest
    import upyog as upy

    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("foobar.txt")
    tempfile.write("foobar")

    dirpath   = str(directory)
    fpath     = str(tempfile)

    assert upy.check_path(fpath)   == fpath
    assert upy.check_path(dirpath) == dirpath

    with pytest.raises(FileNotFoundError):
        upy.check_path("foo")