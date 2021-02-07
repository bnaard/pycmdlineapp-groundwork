import pytest
from pycmdlineapp_groundwork.factory.descriptor import StrDescriptor, AutoStrDescriptor, IntDescriptor, auto
from pycmdlineapp_groundwork.factory.builder import GenericBuildArtifact, GenericBuilder


class ExampleAutoStrDescriptor(AutoStrDescriptor):
    value1_name= auto()
    value2_name= auto()

class ExampleIntDescriptor(IntDescriptor):
    value1_name= 42
    value2_name= auto()

@pytest.fixture
def example_auto_str_descriptor_value():
    yield ExampleAutoStrDescriptor.value1_name

@pytest.fixture
def example_int_descriptor_value():
    yield ExampleIntDescriptor.value1_name


def test_generic_build_artifact():
    artifact= GenericBuildArtifact()
    assert isinstance(artifact, GenericBuildArtifact)

def test_generic_builder_with_generic_artifact(example_auto_str_descriptor_value, example_int_descriptor_value):
    builder= GenericBuilder(example_auto_str_descriptor_value, GenericBuildArtifact, 142, foo= "bar")
    assert builder._count == 0
    assert 142 in builder._fixed_args
    assert "foo" in builder._fixed_kwargs
    assert builder._fixed_kwargs["foo"] == "bar"
    assert example_auto_str_descriptor_value in builder._registry
    assert builder._registry[example_auto_str_descriptor_value] == GenericBuildArtifact

    with pytest.raises(ValueError):
        builder.register(None, GenericBuildArtifact)
    with pytest.raises(ValueError):
        builder.register(example_int_descriptor_value, None)
    with pytest.raises(ValueError):
        builder.register(example_auto_str_descriptor_value, GenericBuildArtifact)

    builder.register(example_int_descriptor_value, GenericBuildArtifact)
    assert example_int_descriptor_value in builder._registry
    assert builder._registry[example_int_descriptor_value] == GenericBuildArtifact
    assert str(builder) == "Builder 'GenericBuilder' building {<ExampleAutoStrDescriptor.value1_name: 'value1_name'>: <class 'pycmdlineapp_groundwork.factory.builder.GenericBuildArtifact'>, <ExampleIntDescriptor.value1_name: 42>: <class 'pycmdlineapp_groundwork.factory.builder.GenericBuildArtifact'>}"


class SpecificBuildArtifact(GenericBuildArtifact):
    def __init__(self, positional_arg: str, foo: int = 12):
        self.positional_arg= positional_arg
        self.keyword_arg= foo

class SpecificBuildArtifactNoPosArg(GenericBuildArtifact):
    def __init__(self, foo: int = 12):
        self.keyword_arg= foo

class SpecificBuildArtifactWithAdditionalArgs(GenericBuildArtifact):
    def __init__(self, positional_arg: str, some_other_pos_arg: int, foo: int = 12, some_other_keyword_arg: str = "baz"):
        self.positional_arg= positional_arg
        self.keyword_arg= foo
        self.some_other_keyword_arg= some_other_keyword_arg
        self.some_other_pos_arg= some_other_pos_arg


def test_generic_builder_with_specific_artifact():
    builder= GenericBuilder(ExampleIntDescriptor.value1_name, SpecificBuildArtifact, "bar", foo= 42)
    obj= builder()
    assert obj is not None
    assert isinstance(obj, GenericBuildArtifact)
    assert isinstance(obj, SpecificBuildArtifact)
    assert obj.positional_arg == "bar"
    assert obj.keyword_arg == 42
    builder= GenericBuilder(ExampleIntDescriptor.value1_name, SpecificBuildArtifact, "johndoe", foo= 142)
    obj= builder()
    assert obj.positional_arg == "johndoe"
    assert obj.keyword_arg == 142
    obj= builder(ExampleIntDescriptor.value1_name)    
    assert obj.positional_arg == "johndoe"
    assert obj.keyword_arg == 142
    with pytest.raises(TypeError):
        obj= builder(ExampleIntDescriptor.value1_name, 99)
    builder.register(ExampleIntDescriptor.value2_name, SpecificBuildArtifactWithAdditionalArgs)
    obj= builder(ExampleIntDescriptor.value2_name, 99)
    assert obj.positional_arg == "johndoe"
    assert obj.keyword_arg == 142
    assert obj.some_other_keyword_arg == "baz"
    assert obj.some_other_pos_arg == 99
    obj= builder(ExampleIntDescriptor.value2_name, 999, some_other_keyword_arg= "thud!")
    assert obj.positional_arg == "johndoe"
    assert obj.keyword_arg == 142
    assert obj.some_other_keyword_arg == "thud!"
    assert obj.some_other_pos_arg == 999
    builder= GenericBuilder(ExampleIntDescriptor.value1_name, SpecificBuildArtifact)
    with pytest.raises(TypeError):
        obj= builder()
    with pytest.raises(TypeError):
        obj= builder(42)
    obj= builder(ExampleIntDescriptor.value1_name, "grzlbf")
    assert obj.positional_arg == "grzlbf"
    assert obj.keyword_arg == 12
    builder= GenericBuilder(ExampleIntDescriptor.value1_name, SpecificBuildArtifactNoPosArg)
    obj= builder(42)
    assert obj.keyword_arg == 12
    obj= builder(foo= 42)
    assert obj.keyword_arg == 42
    builder.register(ExampleIntDescriptor.value2_name, SpecificBuildArtifactWithAdditionalArgs)
    with pytest.raises(TypeError):
        obj= builder(ExampleIntDescriptor.value2_name, 99)
    obj= builder(ExampleIntDescriptor.value2_name, 99, 999)
    assert obj.positional_arg == 99
    assert obj.keyword_arg == 12
    assert obj.some_other_keyword_arg == "baz"
    assert obj.some_other_pos_arg == 999


@pytest.mark.parametrize("fixed_pos_arg, fixed_keyword_arg, flexible_pos_arg, flexible_keyword_arg, expected_result",
    [("bar", 42, 99, None, "obj"), ("bar", 42, None, None, "obj"), (None, None, None, None, "obj"), 
    (42, "bar", None, None, "obj"), (None, 43, None, None, "obj"), (None, "bar", None, None, "obj")])
def test_generic_builder_with_wrong_argument_cases(fixed_pos_arg, fixed_keyword_arg, 
    flexible_pos_arg, flexible_keyword_arg, expected_result):

    builder= GenericBuilder(ExampleIntDescriptor.value1_name, SpecificBuildArtifactWithAdditionalArgs, 
        fixed_pos_arg, bar= fixed_keyword_arg)
    with pytest.raises(TypeError):
        obj= builder(ExampleIntDescriptor.value1_name, flexible_pos_arg, some_other_keyword_arg= flexible_keyword_arg)

    builder= GenericBuilder(ExampleIntDescriptor.value1_name, SpecificBuildArtifactWithAdditionalArgs, 
        fixed_pos_arg, foo= fixed_keyword_arg)
    if expected_result == "obj":
        obj= builder(ExampleIntDescriptor.value1_name, flexible_pos_arg, some_other_keyword_arg= flexible_keyword_arg)
        assert obj.positional_arg == fixed_pos_arg
        assert obj.keyword_arg == fixed_keyword_arg
        assert obj.some_other_keyword_arg == flexible_keyword_arg
        assert obj.some_other_pos_arg == flexible_pos_arg
    elif expected_result == "typeerror":
        with pytest.raises(TypeError):
            obj= builder(ExampleIntDescriptor.value1_name, flexible_pos_arg, some_other_keyword_arg= flexible_keyword_arg)
    else:
        pytest.fail()

