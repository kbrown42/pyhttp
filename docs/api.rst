.. module:: pyhttp

.. _api:

API
===

Servers
--------
The core server class, :class:`BaseServer <pyhttp.servers.BaseServer>`, handles the core functionality like TCP socket creation, accepting connections, and making calls to a :class:`RequestHandler <pyhttp.BaseHttpRequestHandler>`.

.. autoclass:: pyhttp..BaseServer
.. automethod:: pyhttp.BaseServer.serve_forever

Multi-Threading Support
------------------------
Multi-threaded support is implemented through the Mixin pattern in Python. The :class:`~pyhttp.ThreadedingMixin` class overrides methods in :class:`~pyhttp.BaseServer` to allow for handling client requests in a separate thread.  This keeps the :class:`~pyhttp.ThreadedServer` implementation as simple as declaring a class which first inherits from :class:`~pyhttp.ThreadingMixin`.

.. autoclass:: pyhttp.ThreadingMixin
.. automethod:: pyhttp.ThreadingMixin.process_request
.. automethod:: pyhttp.ThreadingMixin.close

.. autoclass:: pyhttp.ThreadedServer


Request Handling
----------------
.. autoclass:: pyhttp.Request
.. autoclass:: pyhttp.BaseHttpRequestHandler

.. automethod:: pyhttp.BaseHttpRequestHandler.get_path

.. automethod:: pyhttp.BaseHttpRequestHandler.list_dir
.. automethod:: pyhttp.BaseHttpRequestHandler.do_file
.. automethod:: pyhttp.BaseHttpRequestHandler.run_cgi

.. autoclass:: pyhttp.requests.SocketWriter
.. automethod:: pyhttp.requests.SocketWriter.write
.. automethod:: pyhttp.requests.SocketWriter.close


