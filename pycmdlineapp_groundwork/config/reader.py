from pathlib import Path
import enum

import yaml
import schema
from deepmerge import always_merger
import tentaclio

from ..utility.typing import FilePathOrBuffer, PathLike
from .generic_configuration import GenericConfiguration





class ConfigurationReader:

    def __init__(self, configuration: GenericConfiguration):
        self._configuration= configuration
        self._read_configuration= None
    
    def load(self):
        pass

    def parse(self):
        pass

    def merge(self):
        always_merger.merge(self._configuration, self._read_configuration)

    def validate(self):
        pass


class ConfigurationStreamReader(ConfigurationReader):
# filepath_or_bufferstr, path object or file-like object

#     Any valid string path is acceptable. The string could be a URL. Valid URL schemes include http, ftp, s3, gs, and file. For file URLs, a host is expected. A local file could be: file://localhost/path/to/table.csv.

#     If you want to pass in a path object, pandas accepts any os.PathLike.

#     By file-like object, we refer to objects with a read() method, such as a file handle (e.g. via builtin open function) or StringIO.
    def __init__(self, filepath_or_buffer: FilePathOrBuffer, configuration: GenericConfiguration):
        super().__init__(configuration= configuration)
        self._filepath_or_buffer= filepath_or_buffer
        
    def load(self):
        if isinstance(self._filepath_or_buffer, str):
            with tentaclio.open( self._filepath_or_buffer, mode="r") as reader:
                self._read_configuration= reader.read()
        elif isinstance(self._filepath_or_buffer, PathLike):
            with tentaclio.open( str(self._filepath_or_buffer), mode="r") as reader:
                self._read_configuration= reader.read()
        else:
            self._read_configuration= self._filepath_or_buffer.read()


class ConfigurationYAMLReader(ConfigurationStreamReader):
    def parse(self):
        result_dict = yaml.safe_load(self._read_configuration)

    def validate(self):
        if not hasattr(self, "_schema") or self._schema is None:
            raise ValueError(f'{self.__class__.__name__}: No schema set, cannot validate loaded configuration.')
        self._configuration= self._schema.validate(self._configuration)


class ConfigurationENVReader(ConfigurationReader):
    def load(self):
        pass

    def parse(self):
        pass

    def validate(self):
        pass
