from typing import Type, TypeVar, Union, List, Dict

from .descriptor import StrDescriptor, IntDescriptor, auto
from .generic_build_artefact import GenericBuildArtifact, TGenericBuildArtifact


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

    def __init__(
        self,
        type_descriptor_key: Union[None, StrDescriptor, IntDescriptor] = None,
        artifact_type: Union[None, Type[TGenericBuildArtifact]] = None,
        *args,
        **kwargs,
    ):
        """Initialize the generic object builder class and register a first Descriptor/Class-to-be-built pair.
        Args:
            type_descriptor_key (Union[StrDescriptor,IntDescriptor]): The enum-derived descriptor identifying the class-object to be built.
            artifact_type: (Type[TGenericBuildArtifact]): The class type to be built. Must be derived from GenericBuildArtifact
            *args, *kwargs: arbitrary positional and/or keyword arguments that are stored and handed to the class-constructor when creating
                one of the registered objects. Kind of fixed arguments that any class built by this builder receives.
        Raises:
            ValueError: In case only one of type_descriptor_key or artifact_type is None, as in this case, it is unclear what to build.
        Returns:
            builder object
        """
        self._count: int = 0
        self._fixed_args: List = list()
        self._fixed_kwargs: Dict = {}
        self.set_fixed_args(*args, **kwargs)
        self._registry: Dict = {}
        if type_descriptor_key is not None and artifact_type is not None:
            self.register(type_descriptor_key, artifact_type)
        elif (type_descriptor_key is not None and artifact_type is None) or (
            type_descriptor_key is None and artifact_type is not None
        ):
            raise ValueError(
                f"{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} or artifact_type {artifact_type} is None. Both need to have a value or both need to be None."
            )
        self.init_hook()

    def __call__(
        self,
        type_descriptor_key: Union[StrDescriptor, IntDescriptor] = None,
        *args,
        **kwargs,
    ) -> TGenericBuildArtifact:
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
        self._count += 1
        if type_descriptor_key is None:
            if self._registry == {}:
                raise ValueError(
                    f"{self.__class__.__name__}: No build artifacts registered, don't know what to build."
                )
            type_descriptor_key = next(iter(self._registry))
        if type_descriptor_key not in self._registry:
            raise ValueError(
                f"{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} not yet registered, don't know what to build."
            )
        return self._registry[type_descriptor_key](
            *self._fixed_args, *args, **self._fixed_kwargs, **kwargs
        )

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
        Builder 'GenericBuilder' building [foo: 1 => MyClass]

        ```
        """
        return f'Builder \'{self.__class__.__name__}\' building [{", ".join([str(descriptor)+" => "+str(classtype.__name__) for descriptor,classtype in self._registry.items()])}]'

    def register(
        self,
        type_descriptor_key: Union[StrDescriptor, IntDescriptor],
        artifact_type: Type[TGenericBuildArtifact],
    ):
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
        Builder 'GenericBuilder' building [foo: 1 => MyClass1, bar: 2 => MyClass2]

        ```
        """
        if type_descriptor_key is None:
            raise ValueError(
                f"{self.__class__.__name__}: type_descriptor_key cannot be None."
            )
        if type_descriptor_key in self._registry:
            raise ValueError(
                f"{self.__class__.__name__}: type_descriptor_key {type_descriptor_key} already registered to build {self._registry[type_descriptor_key]}."
            )
        if artifact_type is None:
            raise ValueError(
                f"{self.__class__.__name__}: artifact_type cannot be None."
            )
        self._registry[type_descriptor_key] = artifact_type

    def set_fixed_args(self, *args, **kwargs) -> None:
        """Add positional and/or key-word arguments to the arguments that will be passed on each build of an
        object to the constructor of the class to be instantiated.
        Args:
            *args: Arbitrary positional arguments (can be no argument or any number of arguments).
            **kwargs: Arbitrary list of keyword arguments (no argument or any number)
        Returns:
            None
        Example:
        ```python
        >>> class MyClass1(GenericBuildArtifact):
        ...     def __init__(self, posarg, keywordarg= None):
        ...         self._arg= posarg
        ...         self._keywordarg= keywordarg
        >>> class MyClass2(GenericBuildArtifact):
        ...     def __init__(self, posarg, additional_posarg, keywordarg=None, additional_keyword_arg= None):
        ...         self._arg= posarg + additional_posarg
        ...         self._keywordarg= keywordarg + additional_keyword_arg
        >>> class MyDescriptor(StrDescriptor):
        ...     foo= auto()
        ...     bar= auto()
        >>> builder= GenericBuilder()
        >>> builder.register(MyDescriptor.foo, MyClass1)
        >>> builder.register(MyDescriptor.bar, MyClass2)
        >>> builder.set_fixed_args(42, keywordarg="johndoe")
        >>> foo_obj= builder(MyDescriptor.foo)
        >>> bar_obj= builder(MyDescriptor.bar, 42, additional_keyword_arg= "baz")
        >>> (foo_obj._arg, foo_obj._keywordarg)
        (42, 'johndoe')
        >>> (bar_obj._arg, bar_obj._keywordarg)
        (84, 'johndoebaz')

        ```
        """
        for arg in args:
            self._fixed_args.append(arg)

        for key, value in kwargs.items():
            self._fixed_kwargs[key] = value

    def init_hook(self) -> None:
        """Called at the end of __init__(). Avoids the need to overwrite __init__() in most cases.

        Example:
        ```python
        >>> class MyClass(GenericBuildArtifact):
        ...     def __init__(self, context= None):
        ...         self._context= context
        >>> class MyDescriptor(IntDescriptor):
        ...     myclass= auto()
        >>> class MyClassBuilder(GenericBuilder):
        ...     def init_hook(self):
        ...         self.set_fixed_args(context= "foobar")
        >>> builder= MyClassBuilder(MyDescriptor.myclass, MyClass)
        >>> obj1= builder(MyDescriptor.myclass)
        >>> obj1._context
        'foobar'

        ```
        """
        pass

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


TGenericBuilder = TypeVar("TGenericBuilder", bound=GenericBuilder)
