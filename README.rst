.. highlight:: shell

=======
pyhttp
=======

.. module:: pyhttp

Running the Program
----------------------

.. Note:: I recommend using a virtual environment tool like virtualenv or anaconda.

Clone the repository ::

    $ git clone https://github.com/kbrown42/pyhttp.git

cd into the top level directory ::

   $ cd pyhttp

Install the package and it's requirements to your local environment ::

   $ pip install .

or ::

   $ python setup.py install

You can then run then start the server in single threaded by running ::

    $ pyhttp serve

The default host:port is localhost:8888. You can also run in multi-threaded mode with ::

    $ pyhttp server --threaded


Command line API
-----------------
Full documentation of the command line app:

.. click:: pyhttp.__main__:pyhttp
    :prog: pyhttp
    :show-nested:


================
Design Overview
================

Single Threaded Server Graph
-----------------------------

.. graphviz:: graphs/single.dot


Multi-Threaded Server Graph
---------------------------

.. graphviz:: graphs/threaded.dot

.. note:: Each thread actually uses its own :class:`RequestHandler <pyhttp.BaseHttpRequestHandler>`.  This is removed in order to fit the diagram appropriately.

.. rubric:: Overview

Our HTTP server is implemented as a command line application using the Click_ framework which makes abstracts away help messages and command line arguments.

Per the design requirements, we have two types of servers that can be run: a single threaded server which handles request sequentially as they arrive, and a multi-threaded server which creates a thread for each new client request.  We implemented a :class:`~pyhttp.BaseServer` which provides the basic connection functionality and provides methods which are overridden in the :class:`~pyhttp.ThreadingMixin` class.  This keeps our code modular, easy to read, and reduces redundant code.

.. rubric:: The Request Response Lifecycle

When the user starts the application from the command line, a server is initialized, bound to the :code:`host:port` specified, and accepts incoming connections continuously in the :meth:`~pyhttp.BaseServer.serve_forever` function. Upon receipt of a client connection, the server passes the connection information off to a :class:`RequestHandler <pyhttp.BaseHttpRequestHandler>` which takes over the work of serving a response.

The RequestHandler is initialized with connection information, an open socket connection and an address, and a base directory to serve from.  This is by default the root directory of our server package.  A Request object is created by the RequestHandler which proceeds to parse the raw HTTP request string.  From this we extract the HTTP method, requested resource path, and HTTP version.  After storing Request headers in a dictionary, we check for query information in the request content in the case of a Post request.  All this information is stored for use by the handler.

Once the request has been parsed, the :meth:`~pyhttp.BaseHTTPRequestHandler.handle` method creates an absolute file path based on the request resource and chooses one of three options.  We can list a directory, serve static file contents, or start a new process which runs one of our CGO scripts.  CGI are contained in a special directory location.  A description of the CGI processing is described below.  By using the :mod:`mimetypes` module in the Python standard library we can send the appropriate mimetype in the Content-Type for almost any file and have the browser render it properly.  Thus, any file which is not in the special cgi-bin directory will have its contents rendered for the user.  In the case of a directory, we retrieve a list of all files contained in the requested location and create hyperlinks that will will lead to those resources.

During the handling of a request a buffer is maintained which contains lines of text that include response data and content for the browser to render.  Once the action is completed, we join all the lines together into a well formed HTTP response byte string and flush the buffer through a :class:`~pyhttp.requests.SocketWriter`, a simple wrapper around the client socket with a file-like API.



CGI Scripts
---------------------------

We implemented two different server side CGI scripts for Project 1 that both display dynamic content generation embedded in an automatic webpage response. 

The first CGI script displays the server up-time, number of logged in users, and current server processor load average. It is implemented by creating a python cgi script to dynamically build the dynamic information into an HTML string that is sent by our server to the client. Each time the user navigates to the UpTime page, the new information is dynamically generated into the served webpage. 

The second CGI script is a General Online Calculator. This script works similarly to UpTime, but allow the user to enter a string of numbers to be computed. The string needs to be valid python syntax and can use the basic math facilities of python. When the user enters the information into the calculator and clicks the 'calculate' button, the HTML page sends the user's input string along with the page path requested to the server. This information is parsed from the path and sent to the calculator CGI script. Again, the dynamic content is generated and served as a page to the client. 

The testing of each of these scripts can be seen in the images below. 

.. Images showing cgi output





.. Links used in documentation
.. _click: http://click.pocoo.org/5/



