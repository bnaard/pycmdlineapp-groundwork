"""Provides an enum-like class defining known config-file types"""

from ..factory.descriptor import AutoStrDescriptor, auto

class ConfigFileTypes(AutoStrDescriptor):
    """Provides an enum-like class defining known config-file types"""
    toml = auto()
    json = auto()
    yaml = auto()
    infer = auto()
    unknown = auto()
