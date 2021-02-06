import pytest
from pycmdlineapp_groundwork.factory.descriptor import StrDescriptor, AutoStrDescriptor, IntDescriptor, auto


class ExampleStrDescriptor(StrDescriptor):
    value1_name= "value1"
    value2_name= "value2"

@pytest.fixture
def example_str_descriptor_value():
    yield ExampleStrDescriptor.value1_name

def test_str_descriptor(example_str_descriptor_value):
    param1= example_str_descriptor_value
    assert isinstance(param1, StrDescriptor)
    assert isinstance(param1, ExampleStrDescriptor)
    assert param1.value == "value1"
    assert param1.name == "value1_name"
    assert ExampleStrDescriptor("value2") == ExampleStrDescriptor.value2_name
    assert ExampleStrDescriptor["value2_name"] == ExampleStrDescriptor.value2_name
    assert ExampleStrDescriptor.allowed_values() == ["value1", "value2"]
    assert ExampleStrDescriptor.allowed_names() == ["value1_name", "value2_name"]
    assert str(param1) == "value1_name: value1"
        


class ExampleAutoStrDescriptor(AutoStrDescriptor):
    value1_name= auto()
    value2_name= auto()

@pytest.fixture
def example_auto_str_descriptor_value():
    yield ExampleAutoStrDescriptor.value1_name

def test_auto_str_descriptor(example_auto_str_descriptor_value):
    param1= example_auto_str_descriptor_value
    assert isinstance(param1, StrDescriptor)
    assert isinstance(param1, AutoStrDescriptor)
    assert isinstance(param1, ExampleAutoStrDescriptor)
    assert param1.value == "value1_name"
    assert param1.name == "value1_name"
    with pytest.raises(Exception):
        assert ExampleAutoStrDescriptor("value1") == ExampleAutoStrDescriptor.value2_name
    assert ExampleAutoStrDescriptor("value1_name") == ExampleAutoStrDescriptor.value1_name

    assert ExampleAutoStrDescriptor["value2_name"] == ExampleAutoStrDescriptor.value2_name
    assert ExampleAutoStrDescriptor.allowed_values() == ["value1_name", "value2_name"]
    assert ExampleAutoStrDescriptor.allowed_names() == ["value1_name", "value2_name"]
    assert str(param1) == "value1_name: value1_name"



class ExampleIntDescriptor(IntDescriptor):
    value1_name= 1
    value2_name= auto()

@pytest.fixture
def example_int_descriptor_value():
    yield ExampleIntDescriptor.value1_name

def test_int_descriptor(example_int_descriptor_value):
    param1= example_int_descriptor_value
    assert isinstance(param1, IntDescriptor)
    assert isinstance(param1, ExampleIntDescriptor)
    assert param1.value == 1
    assert param1.name == "value1_name"
    assert ExampleIntDescriptor(1) == ExampleIntDescriptor.value1_name
    assert ExampleIntDescriptor["value2_name"] == ExampleIntDescriptor.value2_name
    assert ExampleIntDescriptor.allowed_values() == [1,2]
    assert ExampleIntDescriptor.allowed_names() == ["value1_name", "value2_name"]
    assert str(param1) == "value1_name: 1"
