from typing import Type, TypeVar, Union

from .descriptor import StrDescriptor, IntDescriptor, auto
from .generic_build_artefact import GenericBuildArtifact
from .builder import GenericBuilder, TGenericBuildArtifact



TGenericBuilder= TypeVar("TGenericBuilder", bound= GenericBuilder)


class Factory:
    """Collection of object builders to create object based on an enum/Descriptor type.
    Can be directly used with GenericBuilders or specialized builders or can be derived from
    to eg. pre-register builders.
    Inspired by [RealPython](https://realpython.com/factory-method-python/)
    Example:
    ```python
    >>> class MyMessage(GenericBuildArtifact):
    ...     _context= ""
    ...     _text= "" 
    ...     def __str__(self):
    ...         return f'{self._context}: {self._text}'
    >>> class MyMessage1(MyMessage):
    ...     def __init__(self, context, text):
    ...         self._text= text
    ...         self._context= context
    >>> class MyMessage2(MyMessage):
    ...     def __init__(self, context, number):
    ...         self._text= str(number * 42)
    ...         self._context= context
    >>> class MyMessageTypes(IntDescriptor):
    ...     message1= auto()
    ...     message2= auto()
    >>> class MyMessageBuilder(GenericBuilder):
    ...     def init_hook(self):
    ...         self.set_fixed_args(context= "foobar")
    >>> class MyMessageFactory(Factory):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.register_builder(MyMessageTypes.message1, MyMessageBuilder, MyMessage1)
    ...         self.register_builder(MyMessageTypes.message2, MyMessageBuilder, MyMessage2)
    >>> message_provider= MyMessageFactory()
    >>> message1= message_provider(MyMessageTypes.message1, text= "johndoe")
    >>> message2= message_provider(MyMessageTypes.message2, number= 42)
    >>> print(message1)
    foobar: johndoe
    >>> print(message2)
    foobar: 1764

    ```
    """
    def __init__(self):
        self._builder_registry= {}


    def register_builder(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor],\
        builder_type: Union[Type[TGenericBuilder], GenericBuilder],
        artifact_type: Union[Type[TGenericBuildArtifact], None], *args, **kwargs ) -> None:
        if type_descriptor_key is None:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key cannot be None.')
        if type_descriptor_key in self._builder_registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} already registered to build {self._registry[type_descriptor_key]}.')
        if builder_type is None:
            raise ValueError(f'{self.__class__.__name__}: builder_type cannot be None.')
        if not isinstance(builder_type, GenericBuilder) and artifact_type is None:
            raise ValueError(f'{self.__class__.__name__}: artifact_type cannot be None, if builder_type is not an instance of GenericBuilder.')
        if isinstance(builder_type, GenericBuilder):
            self._builder_registry[type_descriptor_key]= builder_type
        else:
            self._builder_registry[type_descriptor_key]= builder_type(type_descriptor_key, artifact_type, *args, **kwargs )

    def __call__(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor] = None, *args, **kwargs) -> TGenericBuildArtifact:
        if type_descriptor_key is None:
            if self._builder_registry == {}:
                raise ValueError(f'{self.__class__.__name__}: No build artifacts registered, don\'t know which builder to use.')
            type_descriptor_key= next(iter(self._builder_registry)) 
        if type_descriptor_key not in self._builder_registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} not yet registered, don\'t know which builder to use.')
        return self._builder_registry[type_descriptor_key](type_descriptor_key, *args, **kwargs)

