import pytest
from pathlib import Path

from pycmdlineapp_groundwork.config.config_file_types import ConfigFileTypes
from pycmdlineapp_groundwork.config.config_file_loaders import (
    determine_config_file_type,
)


@pytest.mark.parametrize(
    "file_path, resulting_type", [(Path("example_cfg1.yaml"), ConfigFileTypes.yaml)]
)
def test_determine_config_file_type(file_path, resulting_type):
    assert determine_config_file_type(file_path) == resulting_type