.. highlight:: shell

=======
pyhttp
=======
cs 560 programming assignment 1
--------------------------------


Running the Program
----------------------
* Clone the repository ::

    $ git clone https://github.com/kbrown42/pyhttp.git

* cd into the top level directory ::

   $ cd pyhttp

* Install the package and it's requirements to your local environment

    Note: I recommend using a virtual environment tool like virtualenv or anaconda. ::

    $ pip install -e .

You can then run then start the server in single threaded mode with: ::

    $ pyhttp serve

The default host:port is localhost:8888. You can also run in multithreaded mode with ::

    $ pyhttp server --threaded

* For help on command line arguments try ::

    $ pyhttp serve --help


================
Design Overview
================
Some design information goes here...
A simple python html web server that is capable of static file serving, directory listing and traversal, cgi script execution, and simple html form processing.  pyhttp is written as our submission for programming assignment 1 in CS 560, Advanced Operating Systems.








