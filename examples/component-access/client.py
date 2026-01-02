# -*- coding: utf-8 -*-

import Pyro5.api
from Pyro5.server import is_private_attribute
from functools import update_wrapper
from server import MyClass # for debug

class ProxyWrap(Pyro5.api.Proxy):
    """Wraps a proxy so that component classes can be accessed"""
    # __pyroAttributes = frozenset(["_pyroCompProxies"])
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._pyroExposedComps = super().__getattr__('__exposed_comps__')() # get exposed comps from Proxy
        self._pyroCompProxies = {}       # dict of the created component proxies
        
    def __getattr__(self, name):
        """Changes the getattr behavior to access proxy class components.
        Exposed class components of the proxy are returned as it's own proxy
        The shared object on the server must have __is_exposed__ and __get_comp_uri__
        methods defined, see ExposeComps class in server.py
        """
        if name in getattr(self,'_pyroExposedComps',[]):
            # generate new proxy on the fly, or get cached one.
            if name in self._pyroCompProxies.keys():
                return self._pyroCompProxies[name]
            else:
                compProxy = ProxyWrap(self.__get_comp_uri__(name))
                self._pyroCompProxies.update({name: compProxy})
                return compProxy
        return super().__getattr__(name)
      
port = 44444
host = 'localhost'
name = 'MyClass'

myClass = ProxyWrap(uri="PYRO:%s@%s:%s"%(name,host,port))   
#myClass = MyClass()   # for debug

print(myClass.func())
print(myClass.func())
print(myClass.Comp.func())
print(myClass.Comp.func())
print(myClass.Comp.Comp.func())
print(myClass.Comp.Comp.func())



