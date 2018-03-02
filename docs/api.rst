.. _api:


.. module:: pyhttp


Servers
========
There are two different server implementations for this project. A :class:`BaseServer <pyhttp.servers.BaseServer>` which handles the TCP socket creation and accepts connections.  :class:`pyhttp.ThreadedServer` overrides methods in :class:`pyhttp.BaseServer` to allow for handling client requests in a separate thread.

.. autoclass:: pyhttp..BaseServer
.. automethod:: pyhttp.BaseServer.serve_forever

Multi-Threading Support
------------------------
.. autoclass:: pyhttp.ThreadedServer

.. autoclass:: pyhttp.ThreadingMixin
.. automethod:: pyhttp.ThreadingMixin.process_request
.. automethod:: pyhttp.ThreadingMixin.close

Request Handling
==================
.. autoclass:: pyhttp.Request
.. autoclass:: pyhttp.BaseHttpRequestHandler
.. automethod:: pyhttp.BaseHttpRequestHandler.get_path
.. automethod:: pyhttp.BaseHttpRequestHandler.list_dir

.. autoclass:: pyhttp.requests.SocketWriter
.. automethod:: pyhttp.requests.SocketWriter.write
.. automethod:: pyhttp.requests.SocketWriter.close


