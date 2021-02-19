import pytest
from pycmdlineapp_groundwork.factory.descriptor import StrDescriptor, AutoStrDescriptor, IntDescriptor, auto
from pycmdlineapp_groundwork.factory.builder import GenericBuildArtifact, GenericBuilder
from pycmdlineapp_groundwork.factory.factory import Factory


class MyMessage(GenericBuildArtifact):
    _context= ""
    _text= "" 
    def __str__(self):
        return f'{self._context}: {self._text}'

class MyMessage1(MyMessage):
    def __init__(self, context, text=""):
        self._text= text
        self._context= context

class MyMessage2(MyMessage):
    def __init__(self, number, context):
        self._text= str(number)
        self._context= context

class MyMessageTypes(IntDescriptor):
    message1= auto()
    message2= auto()
    message3= auto()

class MyMessageBuilder(GenericBuilder):
    def init_hook(self):
        self.set_fixed_args(context= "foobar")


def test_factory():
    message_provider= Factory()
    assert message_provider is not None
    assert message_provider._builder_registry == {}
    with pytest.raises(ValueError):
        message= message_provider(None)

    message1_builder= MyMessageBuilder(MyMessageTypes.message1, MyMessage1)
    message2_builder= MyMessageBuilder(MyMessageTypes.message2, MyMessage2)
    with pytest.raises(ValueError):
        message_provider.register_builder(None)
    message_provider.register_builder(message1_builder)
    with pytest.raises(ValueError):
        message_provider.register_builder(message1_builder)
    with pytest.raises(ValueError):
        message_provider.register_builder(MyMessageBuilder)
    with pytest.raises(ValueError):
        message_provider.register_builder(MyMessageBuilder, MyMessageTypes.message2)
    with pytest.raises(ValueError):
        message_provider.register_builder(MyMessageBuilder, None, MyMessage2)
    with pytest.raises(ValueError):
        message_provider.register_builder(MyMessageBuilder, MyMessageTypes.message1, MyMessage2)
    message_provider.register_builder(MyMessageBuilder, MyMessageTypes.message2, MyMessage2)
    assert len(message_provider._builder_registry.keys()) == 2
    assert MyMessageTypes.message1 in message_provider._builder_registry.keys()
    assert MyMessageTypes.message2 in message_provider._builder_registry.keys()
    assert isinstance(message_provider._builder_registry[MyMessageTypes.message1], MyMessageBuilder)
    assert isinstance(message_provider._builder_registry[MyMessageTypes.message2], MyMessageBuilder)
    
    message= message_provider(None)
    assert isinstance(message, MyMessage1)
    with pytest.raises(ValueError):
        message= message_provider(MyMessageTypes.message3)
    message= message_provider(MyMessageTypes.message2, 24)
    assert str(message) == "foobar: 24"
