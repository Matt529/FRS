from typing import List
from weakref import WeakValueDictionary

from tastypie.api import NamespacedApi

class FRSApi(NamespacedApi):
    
    _refs = WeakValueDictionary()
    
    def __init__(self, api_name="v1", urlconf_namespace=None, **kwargs):
        super().__init__(api_name, urlconf_namespace, **kwargs)
        
        self.__class__._refs[api_name] = self
        
    @classmethod
    def get_instances(cls) -> List[NamespacedApi]:
        return [*cls._refs.values()]
    
    @classmethod
    def get_instance(cls, api_name: str) -> NamespacedApi:
        return cls._refs.get(api_name)
