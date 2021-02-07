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
    """Generic object builder class to be used with the other factory classes. Builds anything that is derived
    from GenericBuildArtifact and that is identified bei either a StrDescriptor or a IntDescriptor enum.
    Can be used to derive own specialized builders.
    Inspired by [RealPython](https://realpython.com/factory-method-python/)
    Example:
    ```python
    >>> class MyClass(GenericBuildArtifact):
    ...     def __init__(self, some_arg):
    ...         self._some= some_arg
    >>> class MyDescriptor(IntDescriptor):
    ...     option1= auto()
    ...     option2= auto()
    >>> class MyFixedTypeBuilder(GenericBuilder):
    ...     def __init__(self):
    ...         super().__init__(MyDescriptor.option1, MyClass)
    >>> builder= MyFixedTypeBuilder()
    >>> obj= builder(some_arg=42)  # has to be a keyword argument
    >>> obj._some
    42

    ```
    """
    def __init__(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor],\
        artifact_type: Type[TGenericBuildArtifact], *args, **kwargs ):
        """Initialize the generic object builder class and register a first Descriptor/Class-to-be-built pair.
        Args:
            type_descriptor_key (Union[StrDescriptor,IntDescriptor]): The enum-derived descriptor identifying the class-object to be built.
            artifact_type: (Type[TGenericBuildArtifact]): The class type to be built. Must be derived from GenericBuildArtifact
            *args, *kwargs: arbitrary positional and/or keyword arguments that are stored and handed to the class-constructor when creating 
                one of the registered objects. Kind of fixed arguments that any class built by this builder receives.
        Returns:
            builder object
        """
        self._count: int= 0
        self._fixed_args= args
        self._fixed_kwargs= kwargs
        self._registry= {}
        self.register(type_descriptor_key, artifact_type)

    def __call__(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor] = None, *args, **kwargs) -> TGenericBuildArtifact:
        """Creates an object identified by type_descriptor_key. The object type has to be registered using register().
        Increases the internal counter counting how many objects the builder has built so far.
        Args:
            type_descriptor_key (Union[StrDescriptor,IntDescriptor]): The enum-derived descriptor identifying the class-object 
                to be built. If type_descriptor_key is left out, the first registered class type is built. In case you leave out
                type_decriptor_key, you mandatorily need to pass keyword-argument to the class built.
            *args, *kwargs: arbitrary positional and/or keyword arguments  handed to the class-constructor when creating 
                one of the registered objects. Kind of "per-build" arguments. These arguments are used additionally to the
                positional/keyword-arguments handed in to the constructor of this builder.
        Returns:
            built object
        Raises:
            ValueError: if type_decriptor_key is not registered or registry is accidentally empty

        Example:
        ```python
        >>> class MyClass(GenericBuildArtifact):
        ...     def __init__(self, some_arg: int ):
        ...         self._some= some_arg
        >>> class MyDescriptor(IntDescriptor):
        ...     myclass= auto()
        >>> builder= GenericBuilder(MyDescriptor.myclass, MyClass)
        >>> obj= builder(MyDescriptor.myclass, 42)
        >>> obj._some
        42
        >>> # obj= builder(4242)   # ERROR: raises TypeError
        >>> obj= builder(some_arg= 4242)
        >>> obj._some
        4242
        
        ```
        """
        self._count+= 1
        if type_descriptor_key is None:
            if self._registry == {}:
                raise ValueError(f'{self.__class__.__name__}: No build artifacts registered, don\'t know what to build.')
            type_descriptor_key= next(iter(self._registry)) 
        if type_descriptor_key not in self._registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} not yet registered, don\'t know what to build.')
        return self._registry[type_descriptor_key](*self._fixed_args, *args, **self._fixed_kwargs, **kwargs)


    def __str__(self):
        """Return a string showing what this builder can build, ie. showing registered Descriptors and class types.
        ```python
        Example:
        >>> class MyClass(GenericBuildArtifact):
        ...     def __init__(self, some_arg: int ):
        ...         self._some= some_arg
        >>> class MyDescriptor(StrDescriptor):
        ...     foo= auto()
        >>> builder= GenericBuilder(MyDescriptor.foo, MyClass)
        >>> print(builder)
        Builder 'GenericBuilder' building {<MyDescriptor.foo: '1'>: <class 'pycmdlineapp_groundwork.factory.builder.MyClass'>}

        ```
        """
        return f'Builder \'{self.__class__.__name__}\' building {self._registry}'

    def register(self, type_descriptor_key: Union[StrDescriptor,IntDescriptor],\
        artifact_type: Type[TGenericBuildArtifact]):
        """Register a type descriptor and its associated class to be built. 
        Args:
            type_descriptor_key (Union[StrDescriptor,IntDescriptor]): The enum-derived descriptor identifying the class-object to be built.
            artifact_type: (Type[TGenericBuildArtifact]): The class type to be built. Must be derived from GenericBuildArtifact
        Returns:
            None
        Raises:
            ValueError: if type_decriptor_key is None, if artifact_type is None or if type_descriptor_key is already 
                registered.
        Example:
        ```python
        >>> class MyClass1(GenericBuildArtifact):
        ...     pass
        >>> class MyClass2(GenericBuildArtifact):
        ...     pass
        >>> class MyDescriptor(StrDescriptor):
        ...     foo= auto()
        ...     bar= auto()
        >>> builder= GenericBuilder(MyDescriptor.foo, MyClass1)
        >>> builder.register(MyDescriptor.bar, MyClass2)
        >>> print(builder)
        Builder 'GenericBuilder' building {<MyDescriptor.foo: '1'>: <class 'pycmdlineapp_groundwork.factory.builder.MyClass1'>, <MyDescriptor.bar: '2'>: <class 'pycmdlineapp_groundwork.factory.builder.MyClass2'>}

        ```
        """
        if type_descriptor_key is None:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key cannot be None.')
        if type_descriptor_key in self._registry:
            raise ValueError(f'{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} already registered to build {self._registry[type_descriptor_key]}.')
        if artifact_type is None:
            raise ValueError(f'{self.__class__.__name__}: artifact_type cannot be None.')
        self._registry[type_descriptor_key]= artifact_type


    def get_count(self) -> int: 
        """Get number of object built so far by this builder instance.
        Returns:
            built object count

        Example:
        ```python
        >>> class MyClass(GenericBuildArtifact):
        ...     pass
        >>> class MyDescriptor(IntDescriptor):
        ...     myclass= auto()
        >>> builder= GenericBuilder(MyDescriptor.myclass, MyClass)
        >>> obj1= builder(MyDescriptor.myclass)
        >>> builder.get_count()
        1
        >>> obj2= builder(MyDescriptor.myclass)
        >>> builder.get_count()
        2

        ```
        """
        return self._count
