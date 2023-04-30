# imports - standard imports
import subprocess as sp

# imports - module imports
from upyutils.util.system import popen
from upyutils.exception   import (
    upyutilsError,
    PopenError,
    DependencyNotFoundError
)

# imports - test imports
import pytest

def test_upyutils_error():
    with pytest.raises(upyutilsError):
        raise upyutilsError

def test_popen_error():
    with pytest.raises(PopenError):
        popen('python -c "from upyutils.exceptions import PopenError; raise PopenError"')

    assert isinstance(
        PopenError(0, "echo foobar"),
        (upyutilsError, sp.CalledProcessError)
    )
    assert isinstance(upyutilsError(), Exception)

def test_dependency_not_found_error():
    assert isinstance(DependencyNotFoundError(), ImportError)