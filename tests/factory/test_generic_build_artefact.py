import pytest
from pycmdlineapp_groundwork.factory.generic_build_artefact import GenericBuildArtifact
from pycmdlineapp_groundwork.factory.descriptor import IntDescriptor, auto
from pycmdlineapp_groundwork.factory.builder import GenericBuilder


class MyClass(GenericBuildArtifact):
    def __init__(self, some_arg):
        self._some= some_arg
    
class MyDescriptor(IntDescriptor):
    myclass= auto()


def test_generic_build_artifact():
    artifact= GenericBuildArtifact()
    assert isinstance(artifact, GenericBuildArtifact)
    builder= GenericBuilder(MyDescriptor.myclass, MyClass, 42)
    obj= builder()
    assert isinstance(obj, MyClass)
    assert obj._some == 42
