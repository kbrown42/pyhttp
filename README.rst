.. highlight:: shell

=======
pyhttp
=======

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

Some design information goes here...
A simple python html web server that is capable of static file serving, directory listing and traversal, cgi script execution, and simple html form processing.  pyhttp is written as our submission for programming assignment 1 in CS 560, Advanced Operating Systems.



CGI
----

:: Corey do this part...

.. rubric:: Some paragraph Heading

Paragraph info....



