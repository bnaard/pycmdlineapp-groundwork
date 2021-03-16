import logging
import logging.config


from schema import Schema


from .default import CONFIG_FILE_LOCAL_DEFAULT, CONFIG_FILE_USERHOME_DEFAULT
from .generic_configuration import GenericConfiguration



class ValidatedConfiguration(GenericConfiguration):
    """Configuration object that has an associated schema powered by [schema](https://pypi.org/project/schema/)-library.
    """
    def __init__(self, schema: Schema):
        """Initializes a validated schema by setting the private property holding the configuration and by 
        associating the `schema` definition.
        Args:
            schema: a dict-structure using [schema](https://pypi.org/project/schema/) library, against which the configuration is validated  
        """
        super().__init__()
        self._schema= schema

    def validate(self):
        """Validate the configuration against the schema associated with this object.
        Uses `schema.validate()`, which returns the validated configuration-dict. Stores the validated configuration
        dict as new configuration. Note: This might lead to transformations (such as uppercasing) as per schema-definition.

        Example:
        ```python
        >>> from io import StringIO
        >>> from schema import Schema, And, Use
        >>> from .reader import ConfigurationYAMLReader
        >>> config_schema= Schema({str: And(str, Use(str.upper)), "johndoe": int})
        >>> cfg= ValidatedConfiguration(config_schema)
        >>> config_text= StringIO('foo: bar\\njohndoe: 42')
        >>> stream_reader= ConfigurationYAMLReader(filepath_or_buffer= config_text, configuration= cfg)
        >>> stream_reader.load()
        >>> stream_reader.parse()
        >>> stream_reader.merge()
        >>> stream_reader.validate()
        >>> stream_reader._configuration._configuration
        {'foo': 'BAR', 'johndoe': 42}

        ```
        """
        if not hasattr(self, "_schema") or self._schema is None: 
            raise ValueError(f'{self.__class__.__name__}: No schema set, cannot validate configuration.')
        self._configuration= self._schema.validate(self._configuration)













# class Config:
#     """Class encapsulating configuration information"""

#     def __init__(self, config_file_userhome=CONFIG_FILE_USERHOME_DEFAULT, config_file_local=CONFIG_FILE_LOCAL_DEFAULT):
#         """Create configuration object, fill with configuration information and initialize loggers

#         Order precedence of sources tried to read to get current configuration (higher number overwrites setting read from lower number):
#         1. default configuration, hard-coded in default.py
#         2. user configuration file configured in default.py, constant
#         3. configuration file dingest.ini in current working directory
#         4. command line processing for selected config values

#         Args:
#             config_file_userhome: file path to ini file in user's home
#             config_file_local: file path to the config file to look for in local directory

#         Raises:
#             SchemaError, YAMLError, Exception

#         Returns:
#             The current configuration (except: input from command line processing).
#         """

#         # get the paths to the user-home and local config file and validate them
#         if config_file_userhome is None or not isinstance(config_file_userhome, str) or config_file_userhome == "":
#             self.config_file_userhome = None
#         else:
#             try:
#                 self.config_file_userhome = os.path.expanduser(
#                     config_file_userhome)
#             except BaseException:
#                 self.config_file_userhome = os.path.expanduser(
#                     CONFIG_FILE_USERHOME_DEFAULT)

#         if config_file_local is None or not isinstance(config_file_local, str) or config_file_local == "":
#             self.config_file_userhome = None
#         else:
#             self.config_file_local = config_file_local
#             if not os.path.exists(self.config_file_local):
#                 self.config_file_local = os.getcwd() + os.sep + CONFIG_FILE_LOCAL_DEFAULT

#         self.dingest_schema = dingest.common.schema.ConfigSchema()

#     def load_base_config(self):
#         """Load dingest base configuration from initialized class members

#         Args:
#             None

#         Raises:
#             SchemaError, YAMLError, Exception

#         Returns:
#             self, an updated DingestConfig instance.
#         """

#         self.config = yaml.safe_load(
#             dingest.common.config_default.CONFIG_DEFAULT_YAML)

#         if self.config_file_userhome is not None:
#             self.load_validate_merge(self.config_file_userhome)

#         if self.config_file_local is not None:
#             self.load_validate_merge(self.config_file_local)

#         logging_config_dict = self.config["logging"]
#         self.config_logging(logging_config_dict)

#         return self

#     def load_validate_merge(self, filepath=""):
#         """Loads a configuration file in YAML format, validates it against a schema and deepmerges it with internal config-dict

#          uses self.load_and_validate_config_file() internally

#          Args:
#              filepath: a file path to a yaml file

#          Raises:
#              SchemaError, YAMLError, Exception

#          Returns:
#              None
#         """
#         if not hasattr(self, 'config'):
#             self.config = {}
#         config_local = self.load_and_validate_config_file(filepath)
#         self.deepmerge_config(self.config, config_local)

#     def config_logging(self, logging_conf: dict = None):
#         """Configure Python logging on basis of DingestConf dictionary object

#             Uses logging to write debug messages if successfully configured
#         Args:
#             logging_conf: the sub-dictionary for logging configuration out of a dingest-conf dict. Structure must be compliant to https://docs.python.org/3/library/logging.html

#         Raises:
#             None

#         Returns:
#             None
#         """
#         logging.config.dictConfig(logging_conf)
#         self.log = logging.getLogger("dingest")
#         self.log.debug(f"Loggers configured: ", [
#                        f"{logger} " for logger in logging_conf])

#     def deepmerge_config(self, base: dict = None, overwrite: dict = None):
#         """Wrapper around deepmerge.always_merger.merge: deepmerging dict-like objects

#             Recurseively walk through base, replacing values from overwrite, if set therein.

#         Args:
#             base: one dict, will be modified with values from overwrite
#             overwrite: dict to merge into base

#         Raises:
#             None

#         Returns:
#             None
#         """
#         if base is not None and overwrite is not None:
#             deepmerge.always_merger.merge(base, overwrite)

#     def load_and_validate_config_file(self, filepath="") -> dict:
#         """Loads a configuration file in YAML format into a dict and validates it against a schema

#         Safely loads the given configuration file using PyYAML library. No checking of the validity of the file-paths is done
#         (needs to be verified before), only a check of the existence of the file in the filesystem is performed.
#         Catches all exceptions, prints an error message to stout and returns an empty dictionary in case of error.

#         Args:
#             filepath: a file path to a yaml file

#         Raises:
#             SchemaError, YAMLError, Exception

#         Returns:
#             A dictionary with the loaded, parsed and validated YAML in the file or an empty dict in case of error.
#         """
#         result_dict = {}

#         # load and parse file safely file if exsts
#         if filepath is not None and filepath != "":
#             if os.path.exists(filepath):
#                 try:
#                     with open(filepath, 'r') as stream:
#                         result_dict = yaml.safe_load(stream)
#                 except yaml.YAMLError as e:
#                     raise Exception(
#                         f"Error parsing config file from {filepath}. {e}") from e
#                 except Exception as e:
#                     raise Exception(
#                         f"Error loading config file from {filepath}. {e}") from e

#         # validate against yaml schema
#         result_dict = self.dingest_schema.validate(result_dict)

#         return result_dict

#     def __call__(self) -> dict:
#         """Provide current configuration dictionary

#         Args:
#             None

#         Raises:
#             None

#         Returns:
#             a dictionary with the current configuration content.
#         """
#         return self.get()

#     def get(self) -> dict:
#         """Provide current configuration dictionary

#         Args:
#             None

#         Raises:
#             None

#         Returns:
#             a dictionary with the current configuration content.
#         """
#         return self.config


# ################################################################################
# # GLOBAL SCOPE EXECUTION
# ################################################################################
# conf = DingestConfig().load_base_config()
