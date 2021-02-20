from typing import Type, TypeVar, Union

from .descriptor import StrDescriptor, IntDescriptor, auto
from .generic_build_artefact import GenericBuildArtifact, TGenericBuildArtifact
from .builder import GenericBuilder, TGenericBuilder


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
    ...         self.register_builder(MyMessageBuilder, MyMessageTypes.message1, MyMessage1)
    ...         self.register_builder(MyMessageBuilder, MyMessageTypes.message2, MyMessage2)
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


    def register_builder(self, builder_type: Union[Type[TGenericBuilder], GenericBuilder],
        type_descriptor_key: Union[StrDescriptor, IntDescriptor, None]= None,
        artifact_type: Union[Type[TGenericBuildArtifact], None]= None ) -> None:
        """Register a builder, either by giving the builders class, the descriptor and the class type it shall create
        or by giving an already instantiated builder object. After registering, calling the factory with a descriptor uses
        the registeredbuilder to build the associated objects.
        Args:
            type_descriptor_key: The enum-derived descriptor identifying the class-object to be built.
            builder_type: The builder used to create instances of the artifact type. Must be derived from GenericBuilder.
            artifact_type: The class type to be built. Must be derived from GenericBuildArtifact. 

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
        >>> message_provider= Factory()
        >>> message1_builder= MyMessageBuilder(MyMessageTypes.message1, MyMessage1)
        >>> message2_builder= MyMessageBuilder(MyMessageTypes.message2, MyMessage2)
        >>> message_provider.register_builder(message1_builder)
        >>> message_provider.register_builder(message2_builder)
        >>> message1= message_provider(MyMessageTypes.message1, text= "johndoe")
        >>> message2= message_provider(MyMessageTypes.message2, number= 42)
        >>> print(message1)
        foobar: johndoe
        >>> print(message2)
        foobar: 1764

        ```
        """
        if builder_type is None:
            raise ValueError(f'{self.__class__.__name__}: builder_type cannot be None.')
        if not isinstance(builder_type, GenericBuilder) and type_descriptor_key is None:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key cannot be None, if builder_type is not an instance of GenericBuilder.')
        if not isinstance(builder_type, GenericBuilder) and artifact_type is None:
            raise ValueError(f'{self.__class__.__name__}: artifact_type cannot be None, if builder_type is not an instance of GenericBuilder.')
        if type_descriptor_key is not None and type_descriptor_key in self._builder_registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} already registered to build {self._builder_registry[type_descriptor_key]}.')
        if isinstance(builder_type, GenericBuilder):
            for type_descriptor_key in builder_type._registry.keys():
                if type_descriptor_key in self._builder_registry:
                    raise ValueError(f'{self.__class__.__name__}: trying to register builder \'{builder_type}\', but type_descriptor_key {type_descriptor_key} already registered in factory to build {self._builder_registry[type_descriptor_key]}.')
                else:
                    self._builder_registry[type_descriptor_key]= builder_type
        else:
            self._builder_registry[type_descriptor_key]= builder_type(type_descriptor_key, artifact_type )



    def __call__(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor] = None, *args, **kwargs) -> TGenericBuildArtifact:
        """Build and return an object referred to by type_descriptor_key using the builder registered for this object type.
        Args:
            type_descriptor_key: The enum-derived descriptor identifying the class-object to be built.
            *args: Positional arguments passed to the registered object builder.
            **kwargs: Keyword arguments passed to the registered object builder. 
        Returns:
            instance of class type (descendant of GenericBuildArtefact) associated with type_descriptor_key
        Example:
        ```python
        >>> class MyMessage(GenericBuildArtifact):
        ...     def __init__(self, context, text):
        ...         self._text= text
        ...         self._context= context
        ...     def __str__(self):
        ...         return f'{self._context}: {self._text}'
        >>> class MyMessageTypes(IntDescriptor):
        ...     message1= auto()
        >>> class MyMessageBuilder(GenericBuilder):
        ...     def init_hook(self):
        ...         self.set_fixed_args(context= "foobar")
        >>> message_provider= Factory()
        >>> message_provider.register_builder(MyMessageBuilder, MyMessageTypes.message1, MyMessage)
        >>> message1= message_provider(MyMessageTypes.message1, text= "johndoe")
        >>> print(message1)
        foobar: johndoe

        ```
        """
        if type_descriptor_key is None:
            if self._builder_registry == {}:
                raise ValueError(f'{self.__class__.__name__}: No build artifacts registered, don\'t know which builder to use.')
            type_descriptor_key= next(iter(self._builder_registry)) 
        if type_descriptor_key not in self._builder_registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} not yet registered, don\'t know which builder to use.')
        return self._builder_registry[type_descriptor_key](type_descriptor_key, *args, **kwargs)

