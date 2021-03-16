
from deepmerge import always_merger


class GenericConfiguration:
    """Base class to store configuration elements as dict.
    """
    def __init__(self):
        """Initializes a configuration object by setting the private property holding the actual
        configuration data to an empty dict.
        """
        self._configuration= {}

    def merge(self, overwriting_configuration: dict):
        """Merges the configuration items represented in overwriting_configuration using deepmerge library.
        Existing configuration items in overwriting_configuration overwrite items in master configuration, 
        items in master configuration but not in overwriting_configuration will be left untouched. 
        Overwriting will only be done on the most elementary level, ie. a structure like `{ "a" : { "b": "c"}, "x": 42 }` will be overwritten
        with a structure `{ "a" : { "b": "d"} }` so that the result will be `{ "a" : { "b": "d"}, "x": 42 }`.
        Only merges, if overwriting_configuration is not empty.
        Args:
            overwriting_configuration: dictionary with one or more elements of a configuration, which will either be added 
                to the private configuration property, or overwrite elements therein, if they keys already exist. 
        """
        if overwriting_configuration is not None and isinstance(overwriting_configuration, dict) and overwriting_configuration != {}:
            always_merger.merge(self._configuration, overwriting_configuration)
