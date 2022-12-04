# imports - standard imports
import subprocess as sp

# imports - module imports
from upyog.util.system import popen
from upyog.exception   import (
    upyogError,
    PopenError,
    DependencyNotFoundError
)

# imports - test imports
import pytest

def test_upyog_error():
    with pytest.raises(upyogError):
        raise upyogError

def test_popen_error():
    with pytest.raises(PopenError):
        popen('python -c "from upyog.exceptions import PopenError; raise PopenError"')

    assert isinstance(
        PopenError(0, "echo foobar"),
        (upyogError, sp.CalledProcessError)
    )
    assert isinstance(upyogError(), Exception)

def test_dependency_not_found_error():
    assert isinstance(DependencyNotFoundError(), ImportError)