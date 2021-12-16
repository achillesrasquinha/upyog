

# imports - module imports
from bpyutils.exception import (
    BpyutilsError
)

# imports - test imports
import pytest

def test_bpyutils_error():
    with pytest.raises(BpyutilsError):
        raise BpyutilsError