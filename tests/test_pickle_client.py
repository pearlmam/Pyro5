# -*- coding: utf-8 -*-

from Pyro5 import config
import Pyro5.api

from test_pickle_server import host, port,name

@Pyro5.api.expose
class TestObject:
    def gen_data(self):
        return [1,2,3,4,5,6,7,8,9,10]

class TestPickle:
    
    def test_enable(self):
        config.PICKLE_ENABLE = False
        config.SERIALIZER = 'pickle'
        uri = "PYRO:%s@%s:%s"%(name,host,port)
        testObject = Pyro5.api.Proxy(uri=uri)
        result = testObject.gen_data()
        print(result)
        
    def test_ssl(self):
        
        config.SSL = True
        config.SSL_CACERTS = "../certs/server_cert.pem"    # to make ssl accept the self-signed server cert
        config.SSL_CLIENTCERT = "../certs/client_cert.pem"
        config.SSL_CLIENTKEY = "../certs/client_key.pem"
        uri = "PYRO:%s@%s:%s"%(name,host,port)
        testObject = Pyro5.api.Proxy(uri=uri)
        result = testObject.gen_data()
        print(result)
        
        
        pass

        
        
        
# import Pyro5.api
# Pyro5.api.serve({TestObject:name},host=host, port=port, use_ns=False)

if __name__ == "__main__":
    test = TestPickle()
    test.test_ssl()
    