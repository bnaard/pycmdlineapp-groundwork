from pathlib import Path
import enum

import yaml
import schema
import tentaclio

from ..utility.typing import FilePathOrBuffer, PathLike
from .generic_configuration import GenericConfiguration
from .validated_configuration import ValidatedConfiguration





class ConfigurationReader:
    """Abstract base class for classes reading configuration from various sources (mostly config files in yaml format)"""
    def __init__(self, configuration: GenericConfiguration):
        """Initializes a configuration reader by setting the configuration object, to where the read configuration 
        will be merged to, to initialize a variable that holds the configuration data read from somewhere and 
        a variable that holds the parsed configuration data (as a python dict)
        Args:
            configuration: reference to master configuration to which the read configuration items will be merged into
        """
        self._configuration= configuration
        self._read_configuration= None
        self._parsed_configuration= None
    
    def load(self):
        """Abstract method to load configuration data. To be overwritten by derived classes reading from concrete sources.
        """
        pass

    def parse(self):
        """Abstract method to parse read configuration data. To be overwritten by derived classes reading from concrete sources.
        """
        pass

    def merge(self):
        """Merges data read and parsed from somewhere into the master configuration using deepmerge library.
        Existing parsed configuration items overwrite items in master configuration, items in master configuration but not
        in parsed configuration will be left untouched.
        Only merges, if parsed configuration is not empty.
        """
        self._configuration.merge(self._parsed_configuration)

    def validate(self):
        """Validate the master configuration against the schema stored with the master configuration object.
        """
        if self._configuration is None or not isinstance(self._configuration, ValidatedConfiguration):
            raise ValueError(f'{self.__class__.__name__}: Trying to validate a non-validated configuration {self._configuration}.')
        self._configuration.validate()


class ConfigurationStreamReader(ConfigurationReader):
    """Configuration reader class that reads its elements from any stream-like sources (eg. files).
    """
    def __init__(self, filepath_or_buffer: FilePathOrBuffer, configuration: GenericConfiguration):
        """Initializes configuration reader to read from filepath_or_buffer into configuration.
        Interface inspired by pands read_*-methods, eg. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        Args:
            filepath_or_bufferstr, path object or file-like object
                Any valid string path, which could be a local file-path or an URL. 
                Valid URL schemes include http, ftp, s3, gs, and file. All that is supported by the 
                underlying library [tentaclio](https://github.com/octoenergy/tentaclio) is allowed. 
                pathlib Path objects are also allowed. 
                A file-like object is anything that has a Python read() method, such as a file handle 
                (e.g. via builtin open function) or StringIO.

        """
        super().__init__(configuration= configuration)
        self._filepath_or_buffer= filepath_or_buffer
        

    def load(self):
        """Depending on the object set as filepath_or_buffer set during object instantiation, this method
        opens a location using [tentaclio](https://github.com/octoenergy/tentaclio) library or directly
        reads the already open file handle.
        The result of the read operation is stored in the object private property _read_configuration.
        """
        if isinstance(self._filepath_or_buffer, str):
            with tentaclio.open( self._filepath_or_buffer, mode="r") as reader:
                self._read_configuration= reader.read()
        elif isinstance(self._filepath_or_buffer, PathLike):
            with tentaclio.open( str(self._filepath_or_buffer), mode="r") as reader:
                self._read_configuration= reader.read()
        else:
            self._read_configuration= self._filepath_or_buffer.read()


class ConfigurationYAMLReader(ConfigurationStreamReader):
    """Specialized class that interprets content read by ConfigurationStreamReader methods as
    YAML data, parses those and stores them in the private property _parsed_configuration.
    """
    def parse(self):
        """Parses read configuration data as YAML text stream using [PyYAML](https://pypi.org/project/PyYAML/).
        """
        self._parsed_configuration = yaml.safe_load(self._read_configuration)


class ConfigurationENVReader(ConfigurationReader):
    def load(self):
        pass

    def parse(self):
        pass

    def validate(self):
        pass
