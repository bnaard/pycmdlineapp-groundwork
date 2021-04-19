"""This module implements methods to load dictonaries from text-based configuration files.

File types are recognized by their suffixes. Currently the following file-types are handled:

Suffixes | File Type | Parser 
------ | ---- | ----------- 
`.json`, `.jsn` | JSON | Python standard-lib [JSON parser](https://docs.python.org/3/library/json.html#json.JSONDecodeError)
`.toml`, `.tml`, `.ini`, `.config`, `.cfg` | TOML/INI | [toml parser](https://pypi.org/project/toml/) 
`.yaml`, `.yml` | YAML | [PyYAML parser](https://pyyaml.org/) 


"""  # noqa: E501

import yaml
import toml
import json
from typing import Any, MutableMapping
from pathlib import Path
from .config_file_types import ConfigFileTypes


class DictLoadError(Exception):
    """Specific exception to harmonize as far as possible
    the exceptions raised when parsing files for dictionaries with different
    libraries (eg. PyYaml)."""

    def __init__(
        self,
        message: str,
        document: str = None,
        position: int = None,
        line_number: int = None,
        column_number: int = None,
    ):
        """Initialize the exception class.
        Args:
            message: an error message from the parsing library describing the nature of the parsing error.
            document: full or parts of the documents parsed into a dict (actual content depends on parsing library)
            position: character position where the parsing error occurred, counting from document start
            line_number: line number in the read file where the parsing error occurred 
            column_number: column number in the line where the parsing error occurred 

        """
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message
        self.document = document
        self.position = position
        self.line_number = line_number
        self.column_number = column_number


def determine_config_file_type(file_path: Path) -> ConfigFileTypes:
    """Determine the file type of a given file from its suffix and return determined type as enum-value 
    Args:
        file_path: path to the file for which the type shall be determined
    Returns:
        enum-value determining the file type or a enum-value for an unknown file type
    """
    if file_path.suffix.lower() in [".json", ".jsn"]:
        return ConfigFileTypes.json
    elif file_path.suffix.lower() in [
        ".toml",
        ".tml",
        ".ini",
        ".config",
        ".cfg",
    ]:
        return ConfigFileTypes.toml
    elif file_path.suffix.lower() in [".yml", ".yaml"]:
        return ConfigFileTypes.yaml
    else:
        return ConfigFileTypes.unknown


def load_dict_from_file(
    file_path: Path, file_type: ConfigFileTypes = ConfigFileTypes.infer
) -> MutableMapping[str, Any]:
    """Load the content of a structured text file into a dictionary using one of the standard parsing libraries (eg. PyYaml).
    Known file-types see: determine_config_file_type
    Args:
        file_path: path to the file to be parsed
        file_type: optional, pre-defines the file-type, if known for sure, else file-type is determined by file name's suffix.
    """
    file_type = (
        determine_config_file_type(file_path)
        if file_type == ConfigFileTypes.infer
        else file_type
    )
    if file_type == ConfigFileTypes.unknown:
        raise ValueError(
            f"Format of config file {str(file_path)} could not be determined to be one"
            f" of [{', '.join(ConfigFileTypes.allowed_names())}]."
        )
    if file_type == ConfigFileTypes.json:
        try:
            return json.loads(file_path.read_text())
        except json.JSONDecodeError as e:
            raise DictLoadError(
                message=e.msg,
                document=e.doc,
                position=e.pos,
                line_number=e.lineno,
                column_number=e.colno,
            )
    elif file_type == ConfigFileTypes.toml:
        try:
            return toml.load(file_path)
        except TypeError as e:
            raise DictLoadError(
                message=f"Invalid file provided {str(file_path)}.",
                document="",
                position=0,
                line_number=0,
                column_number=0,
            )
        except toml.TomlDecodeError as e:
            raise DictLoadError( 
                message=e.msg, # type: ignore
                document=e.doc, # type: ignore
                position=e.pos, # type: ignore
                line_number=e.lineno, # type: ignore
                column_number=e.colno, # type: ignore
            ) 
    elif file_type == ConfigFileTypes.yaml:
        try:
            return yaml.safe_load(file_path.read_text())
        except yaml.YAMLError as e:
            raise DictLoadError(
                message=(
                    "Undetermined error while trying to parse as yaml file"
                    f" {str(file_path)}."
                )
            )
        except yaml.MarkedYAMLError as e:
            raise DictLoadError(
                message=f"{e.note} {e.problem}",
                document=e.context,
                position=e.context_mark,
                line_number=e.problem_mark,
                column_number=0,
            )

    return {}
