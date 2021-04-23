import pytest
from pycmdlineapp_groundwork.config.config_file_types import ConfigFileTypes


def test_config_file_types():
    assert set(ConfigFileTypes.allowed_names()) == set(["json", "toml", "yaml", "infer", "unknown"])
