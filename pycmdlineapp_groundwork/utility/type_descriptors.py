from typing import Sequence, Tuple, Union, Iterable
from collections import namedtuple

class TypeDescriptors:
    class TypeDescriptor:
        _elements: Tuple[str,int,str]
        def __init__(self, name:str=None, key:int=None, description:str=None):
            self.elements= (name, key, description)
        def __str__(self) -> str:
            return f"BuildObjectType ({self.name},{self.key},{self.description})"
        def __iter__(self) -> Tuple[str,int,str]:
            return (self._elements[0],self._element[1],self._elements[2])
        @property
        def name(self) -> str:
            return self._elements[0]
        @property
        def key(self) -> int:
            return self._elements[1]
        @property
        def description(self) -> str:
            return self._elements[2]
        
        
    _types:Sequence[Sequence[TypeDescriptor]]= list()

    def __init__(self):
        pass

    def __getitem__(self, key: int = None) -> Union[TypeDescriptor,None]:
        return next((type_descriptor for type_descriptor in self._types if type_descriptor.key == key), None)

    def __getitem__(self, name: str = None) -> Union[Tuple[str,int,str],None]:
        return next((type_descriptor for type_descriptor in self._types if type_descriptor.name == name), None)

    def __setitem__(self, name: str = None, description: str = None) -> TypeDescriptor:
        return self.append(name= name, description= description) 

    def __getattribute__(self, attribute:str) -> Union[TypeDescriptor,None]:
        next((type_descriptor for type_descriptor in self._types if type_descriptor.name == attribute), None)

    def append(self, name:str = None, description:str = None) -> TypeDescriptor:
        key= self.len(self._types)+1
        self._types.append(self.TypeDescriptor(name if name is not None else "", key, description if description is not None else "" ))
        return key

    def names(self) -> Iterable[str]:
        return (type.name for type in self._types)

    def keys(self) -> Iterable[int]:
        return (type.key for type in self._types)

    def descriptions(self) -> Iterable[str]:
        return (type.description for type in self._types)

    def __call__(self, name:str = None, description:str = None) -> TypeDescriptor:
        return self.append(name= name, description= description)

    def __iter__(self) -> Sequence[TypeDescriptor]:
        return self._types

