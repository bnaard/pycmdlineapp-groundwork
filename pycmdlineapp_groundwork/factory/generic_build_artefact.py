from typing import TypeVar


class GenericBuildArtifact:
    """Empty base class from whoch all objects need to be derived that shall be built with
    GenericBuilder or any derived class
    """

    pass


TGenericBuildArtifact = TypeVar("TGenericBuildArtifact", bound=GenericBuildArtifact)
