import pytest
from pycmdlineapp_groundwork.config.config_file_types import ConfigFileTypes


def test_config_file_types():
    assert ConfigFileTypes.allowed_names == ["json", "toml", "yaml", "infer", "unknown"]
