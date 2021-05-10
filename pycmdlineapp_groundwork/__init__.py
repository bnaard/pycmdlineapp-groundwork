"""PyCmdLineApp-Groundwork, all the boilerplate for jump-starting a Python CLI app."""

__version__= "0.1.0"

from .config.click_config_option import click_config_option
from .config.settings_doc import with_attrs_docs
from .config.config_data_types import ConfigDataTypes
from .config.config_file_loaders import get_settings_config_load_function

from .factory import GenericBuildArtifact, TGenericBuildArtifact, GenericBuilder, TGenericBuilder 
from .factory import IntDescriptor, StrDescriptor, AutoStrDescriptor, auto
from .factory import Factory

