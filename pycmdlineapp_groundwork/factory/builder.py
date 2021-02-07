from typing import Type, TypeVar, Union

from .descriptor import StrDescriptor, IntDescriptor, auto



class GenericBuildArtifact:
    """Empty base class from whoch all objects need to be derived that shall be built with
    GenericBuilder or any derived class
    Example:
    ```python
    >>> class MyClass(GenericBuildArtifact):
    ...     def __init__(self, some_arg):
    ...         self._some= some_arg
    >>> class MyDescriptor(IntDescriptor):
    ...     myclass= auto()
    >>> builder= GenericBuilder(MyDescriptor.myclass, MyClass, 42)
    >>> obj= builder()
    >>> obj._some
    42

    ```
    """
    pass

TGenericBuildArtifact= TypeVar("TGenericBuildArtifact", bound= GenericBuildArtifact)


class GenericBuilder:
    def __init__(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor],\
        artifact_type: Type[TGenericBuildArtifact], *args, **kwargs ):
        self._count: int= 0
        self._fixed_args= args
        self._fixed_kwargs= kwargs
        self._registry= {}
        self.register(type_descriptor_key, artifact_type)

    def __call__(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor] = None, *args, **kwargs) -> TGenericBuildArtifact:
        self._count+= 1
        if type_descriptor_key is None:
            if self._registry == {}:
                raise ValueError(f'{self.__class__.__name__}: No build artifacts registered, don\'t know what to build.')
            type_descriptor_key= next(iter(self._registry)) 
        if type_descriptor_key not in self._registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} not yet registered, don\'t know what to build.')
        return self._registry[type_descriptor_key](*self._fixed_args, *args, **self._fixed_kwargs, **kwargs)


    def __str__(self):
        return f'Builder {self.__class__.__name__} building {self._registry}'

    def register(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor],\
        artifact_type: Type[TGenericBuildArtifact]):
        if type_descriptor_key is None:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key cannot be None.')
        if type_descriptor_key in self._registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} already registered to build {self._registry[type_descriptor_key]}.')
        if artifact_type is None:
            raise ValueError(f'{self.__class__.__name__}: artifact_type cannot be None.')
        self._registry[type_descriptor_key]= artifact_type

    def get_count(self) -> int: 
        return self._count
