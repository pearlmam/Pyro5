Pyro5 with Pickle
=================

This is a fork of the Pyro5 that includes pickle and dill serialization. Use with caution, pickle and dill are insecure! `See how easy it is to exploit pickle <https://arjancodes.com/blog/python-pickle-module-security-risks-and-safer-alternatives/>`_. This fork was developed for use with D-Manage package. The pickle addition is copied and modified from another forked Pyro5 here: `<https://github.com/gst/Pyro5>`_.

Pickle and dill are disabled by default and the default functionality is virtually identical to the main branch. To enable pickle and dill, on both the server and client use the following::

        import Pyro5.api
        Pyro5.api.config.PICKLE_ENABLE=True

Set the serializer the same way as you would with Pyro5, set:: 
        
        Pyro5.api.config.SERIALIZER = 'pickle'
        
The ``config.SERIALIZER`` option only needs to be set on the client because the server side uses whatever serializer the client uses.
      
      
Security: Local Loopback
------------------------
 
Pickle and dill default to be used on only on local loopback ip addresses; that way the socket is only accessible to users with local access. This requirement can be disabled by setting ``config.PICKLE_LOCAL=False``; however this is NOT recommended because anyone on the network can easily mess your server and computer. To access the server from another computer, use port forwarding. Start the server using a local loopback address, like the default ``127.0.0.1``, and use an ssh tunnel on the client to access it::

       $ ssh -L [LOCAL_PORT]:[REMOTE_HOST]:[REMOTE_PORT] user@server

This opens a ``[LOCAL_PORT]`` on the client, that gets forwarded through an ssh connection (``user@server``) to the server ``[REMOTE_HOST]:[REMOTE_PORT]``. For example, to connect to a server running on port ``12345`` on the local loopback ``127.0.0.1``, use the following command  on the client to forward a port::

        $ ssh -L 54321:127.0.0.1:12345 user@server
        
This should appear to ssh into the server like normal, but the port is forwarded. As long as this connection is open, the port will be forwarded. To close the port, disconnect the ssh connection. Check to see if it worked by opening another terminal and executing::
        
        $ ss -ltn | grep 54321
        LISTEN 0      128             127.0.0.1:54321      0.0.0.0:*          
        LISTEN 0      128                 [::1]:54321         [::]:*

Create a proxy on the client like you normally would by connecting to ``host=127.0.0.1``, ``port=54321``. 

Security: SSL Certificates (In Development)
-------------------------------------------

Maybe add an option to check certificates with pickle. The functionality is already there by setting these options:

Server::
        config.SSL = True
        config.SSL_REQUIRECLIENTCERT = True   # enable 2-way ssl
        config.SSL_SERVERCERT = "../certs/server_cert.pem"
        config.SSL_SERVERKEY = "../certs/server_key.pem"
        config.SSL_CACERTS = "../certs/client_cert.pem"
        
Client::
        config.SSL = True
        config.SSL_CLIENTCERT = "../certs/client_cert.pem"
        config.SSL_CLIENTKEY = "../certs/client_key.pem"
        config.SSL_CACERTS = "../certs/server_cert.pem"    # to make ssl accept the self-signed server cert

The pickle enable check hook will also go in protocol.py, and check for config.SSL = True and config.SSL_CLIENTCERT=True? 

Then I need easy instructions on how to generate certificates.

Generate key and puplic cert on server and share with server::
        
        openssl genrsa -out server_key.pem 4096
        openssl req -new -x509 -days 3650 -key server_key.pem -out server_cert.pem
        
Generate key and puplic cert on client::
        
        openssl genrsa -out client_key.pem 4096
        openssl req -new -x509 -days 3650 -key client_key.pem -out client_cert.pem     
        
Push and pull the public client and server certificates from the client::
        scp client_cert.pem user@remote_host:<path/to/cert/location>
        scp user@remote_host:<path/to/cert> ./server_cert.pem
        
There is also a place I can add a hook for more authentication hooks in Pyro5.server::
        class SecureDaemon(Daemon):
            def validateHandshake(self, conn, data):
                cert = conn.sock.getpeercert()
                if not cert:
                    raise errors.CommunicationError("client cert missing")
                
                return super().validateHandshake(conn, data)
            
        Daemon = SecureDaemon   # this overwrites the Daemon with my secure Daemon. I can add a pickle check here and require certificates here.


Pyro5
=====

*Remote objects communication library*

.. image:: https://img.shields.io/pypi/v/Pyro5.svg
    :target: https://pypi.python.org/pypi/Pyro5

.. image:: https://anaconda.org/conda-forge/pyro5/badges/version.svg
    :target: https://anaconda.org/conda-forge/pyro5
    
**Project status: super low maintenance mode. Not really worked on anymore, only reported bugs will be looked at.**

Info
----

Pyro enables you to build applications in which
objects can talk to each other over the network, with minimal programming effort.
You can just use normal Python method calls, and Pyro takes care of locating the right object on the right
computer to execute the method. It is designed to be very easy to use, and to
stay out of your way. But it also provides a set of powerful features that
enables you to build distributed applications rapidly and effortlessly.
Pyro is a pure Python library and runs on many different platforms and Python versions.


Pyro is copyright © Irmen de Jong (irmen@razorvine.net | http://www.razorvine.net).  Please read the file ``license``.

Pyro can be found on Pypi as `Pyro5 <http://pypi.python.org/pypi/Pyro5/>`_.  Source is on Github: https://github.com/irmen/Pyro5
Documentation is here: https://pyro5.readthedocs.io/

Pyro5 is the current version of Pyro. `Pyro4 <https://pyro4.readthedocs.io/>`_ is the predecessor
that only gets important bugfixes and security fixes, but is otherwise no longer being improved.
New code should use Pyro5 if at all possible.


Features
--------

- written in 100% Python so extremely portable, supported on Python 3.9 and newer, and Pypy3
- works between different system architectures and operating systems.
- able to communicate between different Python versions transparently.
- defaults to a safe serializer (`serpent <https://pypi.python.org/pypi/serpent>`_) that supports many Python data types.
- supports different serializers (serpent, json, marshal, msgpack).
- can use IPv4, IPv6 and Unix domain sockets.
- optional secure connections via SSL/TLS (encryption, authentication and integrity), including certificate validation on both ends (2-way ssl).
- lightweight client library available for .NET and Java native code ('Pyrolite', provided separately).
- designed to be very easy to use and get out of your way as much as possible, but still provide a lot of flexibility when you do need it.
- name server that keeps track of your object's actual locations so you can move them around transparently.
- yellow-pages type lookups possible, based on metadata tags on registrations in the name server.
- support for automatic reconnection to servers in case of interruptions.
- automatic proxy-ing of Pyro objects which means you can return references to remote objects just as if it were normal objects.
- one-way invocations for enhanced performance.
- batched invocations for greatly enhanced performance of many calls on the same object.
- remote iterator on-demand item streaming avoids having to create large collections upfront and transfer them as a whole.
- you can define timeouts on network communications to prevent a call blocking forever if there's something wrong.
- remote exceptions will be raised in the caller, as if they were local. You can extract detailed remote traceback information.
- http gateway available for clients wanting to use http+json (such as browser scripts).
- stable network communication code that has worked reliably on many platforms for over a decade.
- can hook onto existing sockets created for instance with socketpair() to communicate efficiently between threads or sub-processes.
- possibility to integrate Pyro's event loop into your own (or third party) event loop.
- three different possible instance modes for your remote objects (singleton, one per session, one per call).
- many simple examples included to show various features and techniques.
- large amount of unit tests and high test coverage.
- reliable and established: built upon more than 20 years of existing Pyro history, with ongoing support and development.

