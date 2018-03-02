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

CGI Scripts
---------------------------

We implemented two different server side CGI scripts for Project 1 that both display dynamic content generation embedded in an automatic webpage response. 

The first CGI script displays the server up-time, number of logged in users, and current server processor load average. It is implemented by creating a python cgi script to dynamically build the dynamic information into an HTML string that is sent by our server to the client. Each time the user navigates to the UpTime page, the new information is dynamically generated into the served webpage. 

The second CGI script is a General Online Calculator. This script works similarly to UpTime, but allow the user to enter a string of numbers to be computed. The string needs to be valid python syntax and can use the basic math facilities of python. When the user enters the information into the calculator and clicks the 'calculate' button, the HTML page sends the user's input string along with the page path requested to the server. This information is parsed from the path and sent to the calculator CGI script. Again, the dynamic content is generated and served as a page to the client. 

The testing of each of these scripts can be seen in the images below. 


CGI
----

:: Corey do this part...

.. rubric:: Some paragraph Heading

Paragraph info....



