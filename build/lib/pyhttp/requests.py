from http import HTTPStatus
import os
from urllib import parse
import html
import socket
import mimetypes
import posixpath
import subprocess
import io



class Request(object):
    """
    A simple class to encapsulate reading and parsing a raw HTTP request string.
    It takes a client socket connection and stores the http command, resource path requested,
    and http version.  It also stores a headers dictionary.

    :param conn: A client socket connection
    """

    def __init__(self, conn):
        req_str = conn.recv(1024)
        print(f'Received request: {req_str}\n')
        print(f'Req has {len(req_str)} bytes\n')
        self._parse_request(req_str.decode())

    def _parse_request(self, req_str):
        # print(f'CMJ_debug: Received request: {req_str}, len {len(req_str)}\n')
        if not len(req_str) == 0:
            header_line = req_str.splitlines()[0]
            headers = header_line.split()
            if len(headers) == 3:
                self.command = headers[0]
                self.path = headers[1]
                print(f'CMJ_debug: self.path= {self.path}\n')
                self.http_ver = headers[2]
        else:
            print(f'CMJ_DEBUG: req_str len 0')
            return

        self._parse_header_fields(req_str)

    def _parse_header_fields(self, req_str):
        lines = req_str.splitlines()[1:]
        self.headers = dict()
        for line in lines:
            if line:
                k, v = line.split(': ')
                self.headers[k] = v


class BaseHttpRequestHandler(object):
    """Base request handler. Parses connection into a :class:`Request <Request>` object

    :param conn: A client connection socket
    :param addr: Client address
    :param server: Server instance that accepted the client connection
    :param directory: Base directory to serve files from.
            Defaults to current working directory
    """

    def __init__(self, conn, addr, server, directory=None):
        self.conn = conn
        self.client_addr = addr
        self.server = server
        self.header_buffer = []
        self.wfile = SocketWriter(conn)
        self.http_version = 'HTTP/1.1'
        self.request = Request(conn)

        if directory is None:
            directory = os.getcwd()

        self.directory = directory
        self.handle()

    def get_path(self, path):
        """
        Takes the path specified in the request header and translates to an
        absolute path on the server's filesystem. Doesn't accept relative
        path markers like '.' or '..' currently.

        :param path: path from http request
        :return: absolute file path on the server's FS
        :rtype: str
        """
        # just in case there are query arguments
        # there shouldn't be for basic filesystem ops
        path = self.request.path
        path = path.split('?')[0]
        # remove any url encodings like %xx
        path = parse.unquote(path)

        # trailing slashes?
        # join request path to server directory
        sub_dirs = path.split('/')
        path = self.directory
        for d in sub_dirs:
            if d != '':
                path = os.path.join(path, d)

        return path

    def list_dir(self, path):
        """
        Takes an absolute path on the server's filesystem and generates
        HTML which lists the path's contents if it is a directory or file contents
        otherwise.

        :param path: an absolute file system path
        :type path: str
        :return: HTML string.
        :rtype: str
        """
        buffer = []
        buffer.append(doctype())
        buffer.append(html_head(f'Directory listing for {path}'))
        buffer.append('<body>')
        buffer.append(h1_header(f'Directory listing for {path}'))
        buffer.append('<hr>')
        files = os.listdir(path)

        buffer.append("<ul>\n")

        for file in files:
            abs_path = os.path.join(path, file)
            ref_name = display = file

            if os.path.isdir(abs_path):
                ref_name = ref_name + '/'
                display = display + '/'

            buffer.append("<li>\n")
            ref_name = parse.quote(ref_name)
            link = f'''<a href="{ref_name}">{display}</a>\n</li>\n'''
            # link = parse.quote(link)
            # link = html.escape(link)
            buffer.append(link)

        buffer.append("</ul>\n")
        buffer.append("</body>\n</html>")

        html_txt = "".join(buffer)
        return html_txt

    def send_response(self, http_status):
        """Writes the http response first line. Expects an HTTPStatus type"""

        if isinstance(http_status, HTTPStatus):
            code = http_status.value
            msg = http_status.name

        line = f'{self.http_version} {code} {msg}\r\n'
        self.header_buffer.append(line)

    def send_header(self, field, value):
        """
        Writes a field: value pair to http response
        :param field: Http response field
        :param value: Http response value
        """
        header = f'{field}: {value}\r\n'
        self.header_buffer.append(header)

    def end_header(self):
        """
        Writes the blank line in http response to signal start of response
        content
        """
        self.header_buffer.append('\r\n')

    def flush_header(self):
        """
        Writes the header buffer to the socket and clears header buffer
        """
        header_bytes = ''.join(self.header_buffer)
        self.wfile.write(header_bytes.encode('utf-8'))
        self.header_buffer = []

    def handle(self):
        path = self.get_path(self.request.path)

        path_params = self.request.path.split('?')
        calc_str = ''

        if len(path_params) >= 2:
            print(f'CMJ_TEST: CGI PARAMS: {path_params[1]}')
            calc_str = path_params[1].split('&')[0][6:]
            print(f'CMJ_TEST: CalcStr: {calc_str}')
            path = path_params[0]

        if os.path.isdir(path):
            print(f'CMJ_TEST: dirispath')
            html_contents = self.list_dir(path)
            if html_contents is not None:
                # Probably should add date information.
                # Not important right now
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Connection', 'close')
                self.end_header()
                self.flush_header()

                self.wfile.write(html_contents.encode('utf-8'))
                self.finish()

        # Otherwise, we're dealing with a file.  Could be cgi or txt
        # or something else.  Handle this later.
        elif os.path.isfile(path):
            print(f'CMJ_TEST: dirisfile')
            base_path, ext = posixpath.splitext(path)
            content_type = mimetypes.types_map.get(ext, 'text/plain')
            f = None
            try:
                f = open(path, 'rb')

            except OSError:
                # TODO: do error handling
                self.send_response(HTTPStatus.NOT_FOUND)

            if f is not None:
                f_size = os.path.getsize(path)

                if path[-3:] == '.py' or path[-4:] == '.cgi':
                    print(f'CMJ_TEST: PY FILE, path:{path}')
                    p = subprocess.Popen(['python2.7', path, calc_str], stdout=subprocess.PIPE)
                    out, err = p.communicate()
                    f2 = io.BytesIO(out)

                    self.send_response(HTTPStatus.OK)
                    content_type = mimetypes.types_map.get(ext, 'text/html')
                    self.send_header('Content-Type', content_type)
                    self.send_header('Connection', 'close')
                    self.send_header('Content-Length', len(out))
                    self.end_header()
                    self.flush_header()

                    self.wfile.write(f2.read())
                else:
                    self.send_response(HTTPStatus.OK)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Connection', 'close')
                    self.send_header('Content-Length', f_size)
                    self.end_header()
                    self.flush_header()

                    self.wfile.write(f.read())

                self.finish()
        else:
            print(f'CMJ_TEST: path not dir or file: {path}')

    def finish(self):
        self.wfile.close()


class SocketWriter(object):
    """
    A simple wrapper around a socket to make interacting with client
    connections similar to doing file writes.  Doesn't do much, but modeled on
    Python's SocketWriter used by the standard library's Http server.  This one doesn't
    inherit from BufferedIOBase but just expects the caller sends appropriately encoded
    bytes to send to client connection.

    :param sock: Open socket connection to client
    """

    def __init__(self, sock):
        self._sock = sock

    def write(self, b):
        """
        Write an encoded byte string to the SocketWriter's client connection.  This is
        unbuffered.

        :param b: An encoded byte string.  We're currently using utf-8 encodings
        :type b: bytes
        :return: Number of bytes written
        """
        self._sock.sendall(b)
        return len(b)

    def close(self):
        """
        Shutdown and close the client connection.
        """
        self._sock.shutdown(socket.SHUT_WR)
        self._sock.close()


def doctype():
    return "<!DOCTYPE html>\n"


def html_head(title=''):
    return f'''
    <html>
    <head>
    <meta charset="UTF-8" content="text/html">
    <title>{title}</title>
    </head>
    '''


def h1_header(txt):
    return f'<h1>{txt}</h1>'
