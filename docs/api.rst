.. _api:


.. module:: pyhttp.servers


Servers
========
There are two different server implementations for this project. A :class:`BaseServer` which handles the TCP socket creation and accepts connections.  :class:`ThreadedServer` overrides methods in :class:`BaseServer` to allow for handling client requests in a separate thread.

.. autoclass:: pyhttp.BaseServer

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


