# imports - standard imports
import subprocess as sp

# imports - module imports
from bpyutils.util.system import popen
from bpyutils.exception   import (
    BPyUtilsError,
    PopenError,
    DependencyNotFoundError
)

# imports - test imports
import pytest

def test_bpyutils_error():
    with pytest.raises(BPyUtilsError):
        raise BPyUtilsError

def test_popen_error():
    with pytest.raises(PopenError):
        popen('python -c "from bpyutils.exceptions import PopenError; raise PopenError"')

    assert isinstance(
        PopenError(0, "echo foobar"),
        (BPyUtilsError, sp.CalledProcessError)
    )
    assert isinstance(BPyUtilsError(), Exception)

def test_dependency_not_found_error():
    assert isinstance(DependencyNotFoundError(), ImportError)