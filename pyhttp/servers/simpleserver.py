import socket
from pyhttp.requests import BaseHttpRequestHandler


class BaseServer(object):
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
                print(f'Received conn from {client_addr}')

                # req = Request(raw_req)
                self.handle_request(client_conn, client_addr)
                # http_response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                # msg = "Hello, World!\r\n\r\n"
                #
                # http_response = http_response.encode('utf-8')
                # msg = msg.encode('utf-8')
                # client_conn.sendall(http_response)
                # client_conn.sendall(msg)
                # print("Sent response")
                # client_conn.close()
                # print("closed connection")
        except KeyboardInterrupt:
            print("Received shutdown...")
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

    def handle_request(self, conn, addr):
        self.requestHandler(conn, addr, self)

