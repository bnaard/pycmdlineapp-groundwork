from typing import Generic
import pytest
from pycmdlineapp_groundwork.config.generic_configuration import GenericConfiguration


def test_generic_configuration():
    cfg= GenericConfiguration()
    assert isinstance(cfg, GenericConfiguration)
    assert hasattr(cfg, "_configuration")
