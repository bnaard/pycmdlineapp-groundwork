import pytest
from schema import Schema
from pycmdlineapp_groundwork.config.generic_configuration import GenericConfiguration
from pycmdlineapp_groundwork.config.validated_configuration import ValidatedConfiguration


def test_validated_configuration():
    dummy_schema= Schema({}, ignore_extra_keys= True)
    cfg= ValidatedConfiguration(dummy_schema)
    assert hasattr(cfg, "_configuration")

