

# imports - standard imports
import subprocess as sp

# imports - module imports
from bpyutils.util.system import popen
from bpyutils.exception   import (
    BpyutilsError,
    PopenError
)

# imports - test imports
import pytest

def test_bpyutils_error():
    with pytest.raises(BpyutilsError):
        raise BpyutilsError

def test_popen_error():
    with pytest.raises(PopenError):
        popen('python -c "from bpyutils.exceptions import PopenError; raise PopenError"')

    assert isinstance(
        PopenError(0, "echo foobar"),
        (BpyutilsError, sp.CalledProcessError)
    )
    assert isinstance(BpyutilsError(), Exception)