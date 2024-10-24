# imports - standard imports
import os, os.path as osp
import subprocess  as sp
from   distutils.spawn import find_executable

# imports - test imports
import pytest
from testutils import PATH

# imports - module imports
from upyog.util.system import (read, write, popen, which, makedirs,
    touch, check_gzip, makepath, remove, make_temp_dir, make_temp_file,
    get_os, unzip, get_files, get_basename, make_archive, move, 
    extract_all)

def test_write(tmpdir):
    directory   = tmpdir.mkdir("tmp")
    tempfile    = directory.join("foobar.txt")
    
    path        = str(tempfile) 
    
    prev, next_ = "foobar", "barfoo"

    write(path, prev)
    assert tempfile.read() == prev

    write(path, next_)
    assert tempfile.read() == prev

    write(path, next_, force = True)
    assert tempfile.read() == next_

@pytest.mark.skipif(os.name == "nt", reason = "requires a UNIX-based OS to run on.")
def test_popen(tmpdir):
    directory = tmpdir.mkdir("tmp")
    dirpath   = str(directory)

    string    = "Hello, World!"

    code, out, err = popen("echo %s" % string,
        output = True)
    assert code == 0
    assert out  == string
    assert not err
    
    env = dict({ "FOOBAR": "foobar" })
    code, out, err = popen("echo $FOOBAR; echo $PATH",
        output = True, env = env)
    assert code == 0
    assert out  == "%s\n%s" % (env["FOOBAR"], os.environ["PATH"])
    assert not err

    with pytest.raises(sp.CalledProcessError):
        code = popen("exit 42")

    errstr = "foobar"
    code, out, err = popen('python -c "raise Exception("%s")"' % errstr,
        output = True, raise_err = False)
    assert code == 1
    assert not out
    assert errstr in err

    filename = "foobar.txt"
    popen("touch %s" % filename, cwd = dirpath)
    assert osp.exists(osp.join(dirpath, filename))

    code = popen("echo $FOOBAR; echo $PATH", quiet = True)
    assert code == 0

def test_which():
    assert which("foobar") == None
    assert which("python") != None

    with pytest.raises(ValueError) as e:
        which("foobar", raise_err = True)

def test_makedirs(tmpdir):
    directory = tmpdir.mkdir("tmp")
    path      = osp.join(str(directory), "foo", "bar")

    makedirs(path)
    assert osp.exists(path)

    makedirs(path, exist_ok = True)
    assert osp.exists(path)

    with pytest.raises(OSError):
        makedirs(path)

def test_touch(tmpdir):
    directory = tmpdir.mkdir("tmp")
    path      = osp.join(str(directory), "foo")

    assert not osp.exists(path)

    touch(path)
    assert osp.exists(path)

def test_check_gzip():
    path_gzip = osp.join(PATH["DATA"], "sample.txt.gz")
    path_txt  = osp.join(PATH["DATA"], "sample.txt")

    assert check_gzip(path_gzip)
    assert not check_gzip(path_txt, raise_err = False)
    
    with pytest.raises(ValueError):
        check_gzip(path_txt)

def test_makepath(tmpdir):
    directory = tmpdir.mkdir("tmp")
    path      = osp.join(str(directory), "foo", "bar", "baz.txt")

    makepath(path)
    assert osp.isfile(path)

from upyog.util.system import (
  pardir,
  BaseShell,
  ShellEnvironment,
  ShellEnvironment,
  copy
)

def test_pardir():
	raise NotImplementedError

def test_remove():
	raise NotImplementedError

def test_make_temp_dir():
	raise NotImplementedError

def test_make_temp_file():
	raise NotImplementedError

def test_base_shell():
	raise NotImplementedError

def test_base_shell___init__():
	raise NotImplementedError

def test_base_shell___call__():
	raise NotImplementedError

def test_ShellEnvironment():
	raise NotImplementedError

def test_shell_environment():
	raise NotImplementedError

def test_shell_environment___enter__():
	raise NotImplementedError

def test_shell_environment___exit__():
	raise NotImplementedError

def test_get_os():
	raise NotImplementedError

def test_unzip():
	raise NotImplementedError

def test_get_files():
	raise NotImplementedError

def test_get_basename():
	raise NotImplementedError

def test_make_archive():
	raise NotImplementedError

def test_move():
	raise NotImplementedError

def test_copy():
	raise NotImplementedError

def test_extract_all():
	raise NotImplementedError



