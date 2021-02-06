Module pycmdlineapp_groundwork.utility.factory
==============================================

Classes
-------

`GenericBuilder(type_descriptior_key: int = None, **kwargs)`
:   

    ### Methods

    `get_count(self) ‑> int`
    :

`GenericObject(**kwargs)`
:   

    ### Methods

    `get(self)`
    :

`ObjectFactory()`
:   

    ### Descendants

    * pycmdlineapp_groundwork.utility.factory.ObjectProvider

    ### Methods

    `create(self, key=None, **kwargs)`
    :

    `get(self, key, **kwargs)`
    :

    `register_builder(self, key=None, builder: pycmdlineapp_groundwork.utility.factory.GenericBuilder = None) ‑> NoneType`
    :

`ObjectProvider()`
:   

    ### Ancestors (in MRO)

    * pycmdlineapp_groundwork.utility.factory.ObjectFactory

    ### Methods

    `register_type(self, name: str = None, description: str = None, builder: pycmdlineapp_groundwork.utility.factory.GenericBuilder = None, **kwargs)`
    :