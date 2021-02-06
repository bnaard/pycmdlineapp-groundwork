from enum import Enum, IntEnum, auto


class StrDescriptor(str, Enum):
    """Defines a str-based enum to be used with command-line options and 
    in dict-like configurations validated with the [schema library](https://pypi.org/project/schema/)"""

    def __str__(self):
        """Return a simplified string representation of the enum's current name and value.
        Example:
        ```python
        >>> class FooBar(StrDescriptor):
        ...     foo= "bar"
        >>> example= FooBar.foo
        >>> print(example)
        foo: bar

        ```
        """
        return f'{self.name}: {self.value}'

    @classmethod
    def allowed_values(cls):
        """Return the _values_ defined in an enum based on StrDescriptor class. This is useful for
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
        """
        return [item.value for item in list(cls)]

    @classmethod
    def allowed_names(cls):
        """Return the _names_ defined in an enum based on StrDescriptor class. This is useful for
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
        """
        return [item.name for item in list(cls)]


class AutoStrDescriptor(StrDescriptor):
    """A convenience-version of the str-based enum to be used with command-line options and 
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
    """
    def _generate_next_value_(name, start, count, last_values):
        """Internal function to generate next value automatically when calling auto()
        see [Python Documentation](https://docs.python.org/3/library/enum.html#using-automatic-values)
        """
        return name    


class IntDescriptor(IntEnum):
    """Defines an int-based enum to be used with command-line options and 
    in dict-like configurations validated with the [schema library](https://pypi.org/project/schema/)"""

    def __str__(self):
        """Return a simplified string representation of the enum's current name and value.
        Example:
        ```python
        >>> class FooBar(IntDescriptor):
        ...     foo= 1
        ...     bar= auto()
        >>> example= FooBar.foo
        >>> print(example)
        foo: 1

        ```
        """
        return f'{self.name}: {self.value}'

    @classmethod
    def allowed_values(cls):
        """Return the _values_ defined in an enum based on IntDescriptor class. This is useful for
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
        """
        return [item.value for item in list(cls)]

    @classmethod
    def allowed_names(cls):
        """Return the _names_ defined in an enum based on IntDescriptor class. This is useful for
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
        """
        return [item.name for item in list(cls)]

