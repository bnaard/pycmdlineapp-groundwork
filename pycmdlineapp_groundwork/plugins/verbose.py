from schema import Schema, And, Use, Optional


class VerbosePlugin:

    def __init__(self, key: str = "verbose", min_verbosity: int= 0, max_verbosity: int= 4):
        self._key= key
        self._min_verbosity= min_verbosity
        self._max_verbosity= max_verbosity
        self._verbosity= min_verbosity

    def get_schema(self) -> Schema:
        return Schema(
            {
                self._key: And(int, Use(lambda v: max(min(v, self._min_verbosity), self._max_verbosity)))
            }
        )

    def get_configuration(self) -> dict:
        return {
            
        }

# command option

# command option validator

# configuration entry

# env variable support

