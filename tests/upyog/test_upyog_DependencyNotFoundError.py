def test_upyog_dependency_not_found_error():
    import pytest
    import upyog as upy

    with pytest.raises(upy.DependencyNotFoundError):
        raise upy.DependencyNotFoundError("foobar")