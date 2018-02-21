from socket import socket


class simpleserver(object):
    def __init__(self):
        pass

    def serve_forever(self, port):
        pass


class Request(object):
    def __init__(self, req_str):
        self._parse_request(req_str)

    def _parse_request(self, req_str):
        m, r, h = self._parse_req_line(req_str)
        self.method = m
        self.resource = r
        self.http_ver = h

    def _parse_header_fields(self, req_str):
        fields_str = req_str.split('\r\n', 1)[1]

        for line in fields_str.split('\r\n'):
            print(line)

    def _parse_req_line(self, req_str):
        line = req_str.split('\r\n', 1)[0]
        method, resource, http_ver = line.split()
        return method, resource, http_ver
