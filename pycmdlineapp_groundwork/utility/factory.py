from typing import Type
from pycmdlineapp_groundwork.utility.type_descriptors import TypeDescriptors


class GenericObject:
    def __init__(self, **kwargs):
        pass

    def get(self):
        return self.message




class GenericBuilder:
    def __init__(self, type_descriptior_key: int = None, **kwargs ):
        if type_descriptior_key is None:
            raise ValueError("GenericBuilder: type_descriptor_key cannot be None.")
        self._type_descriptor_key= type_descriptior_key
        
    def __call__(self, **kwargs) -> None:
        pass

    def get_count(self) -> int: 
        return 0


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


class ObjectProvider(ObjectFactory):
    def __init__(self):
        super().__init__()
        self._type_descriptors: TypeDescriptors = TypeDescriptors()
        return self

    def register_type(self, name: str = None, description: str = None, builder: GenericBuilder= None, **kwargs):
        if name is not None and description is not None:
            type_descriptor_key= self._type_descriptors[str]= description
            self.register_builder( type_descriptor_key, builder(**kwargs)\
                if builder is not None else GenericBuilder(type_descriptor_key= type_descriptor_key, **kwargs) )
