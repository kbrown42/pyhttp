.. _api:


.. module:: pyhttp.servers


Server
========
There are two different server implementations for this project. A :class:`BaseServer` which handles the TCP socket creation and accepts connections.  :class:`ThreadedServer` overrides methods in :class:`BaseServer` to allow for handling client requests in a separate thread.

.. autoclass:: pyhttp.BaseServer

Multi-Threading Support
------------------------
.. autoclass:: pyhttp.ThreadedServer
.. autoclass:: pyhttp.ThreadingMixin
.. automethod:: pyhttp.ThreadingMixin.process_request

Request Handling
==================
.. autoclass:: pyhttp.Request
.. autoclass:: pyhttp.BaseHttpRequestHandler
.. autoclass:: pyhttp.requests.SocketWriter


