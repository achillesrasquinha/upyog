from bpyutils.config  import Settings, environment
from bpyutils         import __version__

def test_settings():
    settings = Settings()
    settings.get("version") == __version__

def test_environment():
    details = environment()

    assert all((k in details for k in ("version", "python_version", "os",
        "config"))) #, "pip_executables")))

    return details

import pytest

from bpyutils.config import (
  get_config_path,
  Configuration
)

def test_get_config_path():
	raise NotImplementedError

def test_configuration():
	raise NotImplementedError

def test_configuration___init__():
	raise NotImplementedError

def test_configuration___del__():
	raise NotImplementedError

def test_configuration_read():
	raise NotImplementedError

def test_configuration_write():
	raise NotImplementedError

def test_configuration_get():
	raise NotImplementedError

def test_configuration_set():
	raise NotImplementedError

def test_settings___init__():
	raise NotImplementedError

def test_settings__init():
	raise NotImplementedError

def test_settings_get():
	raise NotImplementedError

def test_settings_set():
	raise NotImplementedError

def test_settings_to_dict():
	raise NotImplementedError



