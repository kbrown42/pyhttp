import socket
from pyhttp.requests import BaseHttpRequestHandler


class BaseServer(object):
    """
    Basic class for a simple http server.  Handles client connections and passes off
    to a RequestHandler class.
    """
    def __init__(self, host='localhost', port=8888,
                 requestHandler=BaseHttpRequestHandler):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.requestHandler = requestHandler

    def serve_forever(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f'Serving at {self.host}:{self.port}')
        try:
            while True:
                client_conn, client_addr = self.socket.accept()
                self.handle_request(client_conn, client_addr)

        except KeyboardInterrupt:
            print("Received shutdown...")
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

    def handle_request(self, conn, addr):
        self.requestHandler(conn, addr, self)

