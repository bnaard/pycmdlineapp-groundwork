"""PyCmdLineApp-Groundwork, all the boilerplate for jump-starting a Python CLI app."""

__version__= "0.1.0"

from climatecontrol.ext.pydantic import Climate as c
from climatecontrol.cli_utils import click_settings_file_option

from .factory import GenericBuildArtifact, TGenericBuildArtifact, GenericBuilder, TGenericBuilder 
from .factory import IntDescriptor, StrDescriptor, AutoStrDescriptor, auto
from .factory import Factory

