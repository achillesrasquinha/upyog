def test_upyog_is_python_version():
    import sys

    import upyog as upy

    major   = sys.version_info.major
    minor   = sys.version_info.minor
    micro   = sys.version_info.micro
    release = sys.version_info.releaselevel
    serial  = sys.version_info.serial

    assert upy.is_python_version(
        major   = major,
        minor   = minor,
        micro   = micro,
        release = release,
        serial  = serial
    ) == True
    assert upy.is_python_version(major = major + 1) == False
    assert upy.is_python_version(minor = minor + 1) == False
    assert upy.is_python_version(micro = micro + 1) == False

    assert upy.is_python_version(
        major   = major + 1,
        minor   = minor,
        micro   = micro + 1,
        release = release,
        serial  = serial + 1
    ) == False