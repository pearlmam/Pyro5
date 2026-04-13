# -*- coding: utf-8 -*-

from Pyro5 import config
import Pyro5.api

host = "localhost"
port = 44444
name = "testObject"

config.PICKLE_ENABLE = True

@Pyro5.api.expose
class TestObject:
    def gen_data(self):
        return [1,2,3,4,5,6,7,8,9,10]


def test_ssl():
    config.SSL = True
    config.SSL_REQUIRECLIENTCERT = True   # enable 2-way ssl
    config.SSL_SERVERCERT = "../certs/server_cert.pem"
    config.SSL_SERVERKEY = "../certs/server_key.pem"
    config.SSL_CACERTS = "../certs/client_cert.pem"


if __name__ == "__main__":
    test_ssl()

    Pyro5.api.serve({TestObject:name},host=host, port=port, use_ns=False)
    