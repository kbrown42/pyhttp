import socket
from pyhttp.requests import BaseHttpRequestHandler
import threading


class BaseServer(object):
    """
    Basic class for a simple http server.  Accepts client connections and passes off
    to a :class:`RequestHandler <BaseHttpRequestHandler>` class to for processing and responding.

    :param host: Host address to listen on
    :type host: str
    :param port: Port to listen on
    :type port: int
    """

    def __init__(self, host='localhost', port=8888,
                 request_handler=BaseHttpRequestHandler):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.requestHandler = request_handler

    def serve_forever(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f'Serving at {self.host}:{self.port}')
        try:
            while True:
                client_conn, client_addr = self.socket.accept()
                self.process_request(client_conn, client_addr)

        except KeyboardInterrupt:
            self.close()

    def process_request(self, conn, addr):
        """
        Calls finish request.  Serves as one layer of indirection
        to allow for overriding by a threading mixin.
        :param conn: Open client socket
        :param addr: Client socket address
        """
        self.finish_request(conn, addr, self)

    def finish_request(self, conn, addr):
        self.requestHandler(conn, addr, self)

    def close(self):
        # Not sure that we need this first line
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


class ThreadingMixin:
    """
    A threading mixing class that overrides the :func:`process_request`
    function.  Rather than immediately calling the request handler class,
    it creates a processing thread whose target function is
    :func:`threaded_process_request`.  Also keeps track of all threads created
    and waits for them to finish before closing the connection.
    """
    _threads = None

    def process_request(self, conn, addr):
        """
        Overrides :func:`process_request` in :class:`BaseServer`.  Passes
        arguments to a function to be run in separate thread.  Stores the thread
        in the  class attribute list :attr:`_threads`.

        :param conn: Open client socket
        :param addr: Client socket address
        """
        thread = threading.Thread(target=self.threaded_process_request,
                                  args=(conn, addr))
        thread.daemon = False
        if self._threads is None:
            self._threads = []

        self._threads.append(thread)
        thread.start()

    def threaded_process_request(self, conn, addr):
        self.finish_request(conn, addr)

    def close(self):
        """"""
        super(ThreadingMixin, self).close()
        threads = self._threads
        self._threads = None
        if threads is not None:
            for thread in threads:
                thread.join()


class ThreadedServer(ThreadingMixin, BaseServer):
    """
    Uses the basic functionality and call api of BaseServer.
    Overrides the initial processing of a request to put it into a thread.
    For details see :class:`ThreadingMixin <pyhttp.ThreadingMixin>`
    """
    pass



