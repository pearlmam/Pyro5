# -*- coding: utf-8 -*-

import Pyro5.api
from Pyro5.server import is_private_attribute
from server import MyClass

from IPython import get_ipython

# def proxywrap_completer(self, event):
#     """
#     Return a list of attribute names for tab completion.
#     This is called by IPython when you type: ProxyWrap.<TAB>
#     """
#     try:
#         # Attempt to call __dir__ on the object
#         return dir(self)
#     except Exception:
#         return []

# # Register the completer for ProxyWrap
# ip = get_ipython()
# ip.set_hook('complete_object', proxywrap_completer, str_key='ProxyWrap')


class ProxyWrap():
    """Wraps a proxy so that component classes can be accessed"""
    def __init__(self,proxy=None,uri=None):
        if proxy:
            self._proxy = proxy          # the proxy to be wrapped
        elif uri:
            self._proxy = Pyro5.api.Proxy(uri)
        else:
            raise Exception("Input 'proxy' or 'uri' must be defined")
        self._compProxies = {}       # dict of the created component proxies
    
    def __dir__(self):
        base = set(super().__dir__())
        try:
            components = set(self._compProxies.keys())
            parent_attrs = set(dir(self._proxy))
        except Exception:
            components = set()
            parent_attrs = set()
        return sorted(base | components | parent_attrs)

    
    def __getattr__(self, name):
        """Changes the getattr behavior to access proxy components
        private methods of ProxyWrap are returned
        exposed class components of the proxy are returned as it's own proxy
        The shared object on the server must have __exposed_comps__ and __get_comp_uri__
        methods defined, see ExposeComps class in server.py/
        """

        if is_private_attribute(name):
            return getattr(self, name)
        if name in self._compProxies.keys():
            return self._compProxies[name]
        try:
            uri = self._proxy.__get_comp_uri__(name)
        except Exception:
            try:
                return getattr(self._proxy, name)
            except AttributeError:
                raise AttributeError(name)
        compProxy = ProxyWrap(uri=uri)
        self._compProxies[name] = compProxy
        return compProxy
    
    def __reduce__(self):
        raise TypeError(
            f"'{self.__class__.__name__}' objects are not picklable. "
            "Create a new facade inside each process."
            )
    def __copy__(self):
        raise TypeError(f"'{self.__class__.__name__}' cannot be copied")

    def __deepcopy__(self, memo):
        raise TypeError(f"'{self.__class__.__name__}' cannot be deep-copied")
    
    
    # def __getattr__(self, name):
    #     """Changes the getattr behavior to access proxy components
    #     private methods of ProxyWrap are returned
    #     exposed class components of the proxy are returned as it's own proxy
    #     The shared object on the server must have __exposed_comps__ and __get_comp_uri__
    #     methods defined, see ExposeComps class in server.py/
    #     """
    #     if is_private_attribute(name):
    #         return getattr(self,name)    # returns ProxyWrap attr
    #     comps = self._proxy.__exposed_comps__()
    #     if name in comps:
    #         # generate new proxy on the fly, or get cached one.
    #         if name in self._compProxies.keys():
    #             return self._compProxies[name]
    #         else:
    #             compProxy = ProxyWrap(uri=self._proxy.__get_comp_uri__(name))
    #             self._compProxies.update({name: compProxy})
    #             return compProxy
    #     else:
    #         return getattr(self._proxy,name)
        
        
        
        
      
port = 44444
host = 'localhost'
name = 'MyClass'

myClass = ProxyWrap(uri="PYRO:%s@%s:%s"%(name,host,port))   
# myClass = MyClass()   # for debug

# print(myClass.func())
# print(myClass.func())
# print(myClass.Comp.func())
# print(myClass.Comp.func())
# print(myClass.Comp.Comp.func())
# print(myClass.Comp.Comp.func())



