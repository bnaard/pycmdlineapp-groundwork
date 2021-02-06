Module pycmdlineapp_groundwork.factory.descriptor
=================================================

Classes
-------

`AutoStrDescriptor(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   A convenience-version of the str-based enum to be used with command-line options and 
    in dict-like configurations validated with the schema library. If enum-names and values
    can be identical, the use of enum's auto() feature reduces boilerplate code.
    Example:
    ```python
    >>> from schema import Schema, And, Or, Use
    >>> class FooBar(AutoStrDescriptor):
    ...     foo=auto()
    ...     john=auto()
    >>> allowed= FooBar.allowed_names()
    >>> allowed
    ['foo', 'john']
    >>> # Create a schema that accepts a dict with a key 'name' of type str, lowercases it, checks it against
    >>> # the names defined in enum (['foo', 'john']) and returns the respective enum-type instead of the original str
    >>> # note the [] in 'FooBar[v]' in the last 'Use'-term, where the names are retrieved from the enum.
    >>> schema= Schema({'name': And(str, Use(str.lower), Or(*allowed), Use(lambda v: FooBar[v]))}) 
    >>> schema.validate({'name': 'FOO'})
    {'name': <FooBar.foo: 'foo'>}
    
    ```

    ### Ancestors (in MRO)

    * pycmdlineapp_groundwork.factory.descriptor.StrDescriptor
    * builtins.str
    * enum.Enum

`IntDescriptor(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   Defines an int-based enum to be used with command-line options and 
    in dict-like configurations validated with the [schema library](https://pypi.org/project/schema/)

    ### Ancestors (in MRO)

    * enum.IntEnum
    * builtins.int
    * enum.Enum

    ### Static methods

    `allowed_names()`
    :   Return the _names_ defined in an enum based on IntDescriptor class. This is useful for
        feeding the allowed names list into a [schema](https://pypi.org/project/schema/) definition
        and to translate them into enum-types instead of working with int's throughout the application.
        Pendant to allowed_names() in StrDescriptor class.
        Example:
        ```python
        >>> from schema import Schema, And, Or, Use
        >>> class FooBar(IntDescriptor):
        ...     foo=42
        ...     john=auto()
        >>> allowed= FooBar.allowed_names()
        >>> allowed
        ['foo', 'john']
        >>> # Create a schema that accepts a dict with a key 'name' of type int, checks it against
        >>> # the names defined in enum (['foo', 'john']) and returns the respective enum-type instead of the original int
        >>> # note the [] in 'FooBar[v]' in the last 'Use'-term, where the names are retrieved from the enum.
        >>> schema= Schema({'name': And(str, Or(*allowed), Use(lambda v: FooBar[v]))}) 
        >>> schema.validate({'name': 'foo'})
        {'name': <FooBar.foo: 42>}
        
        ```

    `allowed_values()`
    :   Return the _values_ defined in an enum based on IntDescriptor class. This is useful for
        feeding the allowed values list into a [schema](https://pypi.org/project/schema/) definition
        and to translate them into enum-types instead of working with int's throughout the application.
        Pendant to allowed_values() in StrDescriptor class.
        Example:
        ```python
        >>> from schema import Schema, And, Or, Use
        >>> class FooBar(IntDescriptor):
        ...     foo=42
        ...     john=auto()
        >>> allowed= FooBar.allowed_values()
        >>> allowed
        [42, 43]
        >>> # Create a schema that accepts a dict with a key 'name' of type int, checks it against
        >>> # the values defined in enum ([42, 43]) and returns the respective enum-type instead of the original int
        >>> # note the () in 'FooBar(v)' in the last 'Use'-term, where the names are retrieved from the enum.
        >>> schema= Schema({'name': And(int, Or(*allowed), Use(lambda v: FooBar(v)))}) 
        >>> schema.validate({'name': 42})
        {'name': <FooBar.foo: 42>}
        
        ```

`StrDescriptor(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   Defines a str-based enum to be used with command-line options and 
    in dict-like configurations validated with the [schema library](https://pypi.org/project/schema/)

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Descendants

    * pycmdlineapp_groundwork.factory.descriptor.AutoStrDescriptor

    ### Static methods

    `allowed_names()`
    :   Return the _names_ defined in an enum based on StrDescriptor class. This is useful for
        feeding the allowed names list into a [schema](https://pypi.org/project/schema/) definition
        and to translate them into enum-types instead of working with str throughout the application.
        Pendant to allowed_values() and useful when values shall have a different purpose. For example, 
        names can be used as input from config-file structures or command-line arguments/options, while
        values contain long descriptions.
        Example:
        ```python
        >>> from schema import Schema, And, Or, Use
        >>> class FooBar(StrDescriptor):
        ...     foo="The bar that is foo"
        ...     john="The guy who is named doe"
        >>> allowed= FooBar.allowed_names()
        >>> allowed
        ['foo', 'john']
        >>> # Create a schema that accepts a dict with a key 'name' of type str, lowercases it, checks it against
        >>> # the names defined in enum (['foo', 'john']) and returns the respective enum-type instead of the original str
        >>> # note the [] in 'FooBar[v]' in the last 'Use'-term, where the names are retrieved from the enum.
        >>> schema= Schema({'name': And(str, Use(str.lower), Or(*allowed), Use(lambda v: FooBar[v]))}) 
        >>> schema.validate({'name': 'FOO'})
        {'name': <FooBar.foo: 'The bar that is foo'>}
        
        ```

    `allowed_values()`
    :   Return the _values_ defined in an enum based on StrDescriptor class. This is useful for
        feeding the allowed values list into a [schema](https://pypi.org/project/schema/) definition
        and to translate them into enum-types instead of working with str throughout the application.
        Example:
        ```python
        >>> from schema import Schema, And, Or, Use
        >>> class FooBar(StrDescriptor):
        ...     foo="bar"
        ...     john="doe"
        >>> allowed= FooBar.allowed_values()
        >>> allowed
        ['bar', 'doe']
        >>> # Create a schema that accepts a dict with an key 'name' of type str, lowercases it, checks it against
        >>> # the values defined in enum (['bar', 'doe']) and returns the respective enum-type instead of the original str
        >>> # note the () in 'FooBar(v)' in the last 'Use'-term, where the names are retrieved from the enum.
        >>> schema= Schema({'name': And(str, Use(str.lower), Or(*allowed), Use(lambda v: FooBar(v)))}) 
        >>> schema.validate({'name': 'Doe'})
        {'name': <FooBar.john: 'doe'>}
        
        ```