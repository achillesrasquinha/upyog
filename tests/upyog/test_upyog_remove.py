def test_upyog_remove(tmpdir):
    import pytest

    import upyog as upy
    import os.path as osp

    # upy.remove
    # with tmpdir.
    f1 = tmpdir.mkdir("foodir").join("test_file")
    f1.write("foobar")

    upy.remove(f1, recursive = True)
    assert not osp.exists("tmpdir")

    f2 = tmpdir.mkdir("bardir").join("test_file")
    f2.write("barbaz")

    with pytest.raises(OSError):
        upy.remove("bardir")

    upy.remove(f2)
    assert not osp.exists("bardir/test_file")