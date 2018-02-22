import socket
from pyhttp.requests import BaseHttpRequestHandler
import threading


class BaseServer(object):
    """
    Basic class for a simple http server.  Handles client connections and passes off
    to a RequestHandler class.
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
        :param conn: client socket making request
        :param addr: address of client making request
        """
        self.finish_request(conn, addr, self)

    def finish_request(self, conn, addr):
        self.requestHandler(conn, addr, self)

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


class ThreadingMixin:
    _threads = None

    def process_request(self, conn, addr):
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
    """
    pass



