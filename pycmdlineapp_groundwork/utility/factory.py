from typing import Sequence, Tuple, Union
from collections import namedtuple

class BuildObjectTypes:
    class BuildObjectType:
        _elements: Tuple[str,int,str]

        @property
        def name(self) -> str:
            return self._elements[0]
        @property
        def key(self) -> int:
            return self._elements[1]
        @property
        def description(self) -> str:
            return self._elements[2]

    _types:Sequence[Sequence[Tuple[str,int,str]]]= list()

    def __init__(self):
        pass

    def __getitem__(self, key: int = None) -> Union[Tuple[str,int,str],None]:
        return next(((aname,akey,adescription) for aname,akey,adescription in self._types if akey == key), None)

    def __getitem__(self, name: str = None) -> Union[Tuple[str,int,str],None]:
        return next(((aname,akey,adescription) for aname,akey,adescription in self._types if aname == name), None)

    def __setitem__(self, name: str = None, description: str = None) -> Tuple[str,int,str]:
        return self.add(name= name, description= description) 


    def __getattribute__(self, attribute:str) -> Union[Tuple[str,int,str],None]:
        next(((aname,akey,adescription) for aname,akey,adescription in self._types if aname == attribute), None)


    def add(self, name:str = None, description:str = None) -> Tuple[str,int,str]:
        key= self.len(self._types)+1
        self._types.append((name if name is not None else "", key, description if description is not None else "" ))
        return self._types[-1]

    def __call__(self, name:str = None, description:str = None) -> Tuple[str,int,str]:
        return self.add(name= name, description= description)



class GenericBuilder:
    def __init__(self):
        self._message_count = 0   

    def __call__(self) -> None:
        self._message_count += 1

    def get_count(self) -> int: 
        return self._message_count


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key = None, builder: GenericBuilder = None) -> None:
        if key is None:
            raise ValueError(key)
        if builder is None or not isinstance( builder, GenericBuilder ):
            raise ValueError(builder)
        self._builders[ int(key) ] = builder

    def create(self, key = None, **kwargs):
        if key is None:
            raise ValueError(key)
        builder = self._builders.get(int(key))
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
   
    def get(self, key, **kwargs):
        return self.create(key, **kwargs)

    def __call__(self, key, **kwargs):
        return self.create(key, **kwargs)