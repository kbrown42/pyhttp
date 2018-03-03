from http import HTTPStatus
import os
from urllib import parse
import socket
import mimetypes
import subprocess
import io


class Request(object):
    """
    A simple class to encapsulate reading and parsing a raw HTTP request string.
    It takes a client socket connection and stores the http command, resource path requested,
    and http version.  It also stores a headers dictionary.

    :param conn: A client socket connection
    """
    POST = 'POST'
    GET = 'GET'

    def __init__(self, conn):
        req_str = conn.recv(1024)
        self.method = ''
        self.path = ''
        self.http_ver = ''
        self.query_params = ''
        self.headers = dict()

        self._parse_request(req_str.decode())

    def _parse_request(self, req_str):
        if not len(req_str) == 0:
            header_line = req_str.splitlines()[0]
            headers = header_line.split()
            if len(headers) == 3:
                self.method = headers[0]
                self.path = headers[1]
                self.http_ver = headers[2]
            else:
                raise RequestParseError(req_str)
        else:
            raise RequestParseError(req_str)

        self._parse_header_fields(req_str)

    def _parse_header_fields(self, req_str):
        lines = req_str.splitlines()[1:]

        for line in lines:
            if line:
                vals = line.split(': ')
                # We're dealing with request header fields
                if len(vals) == 2:
                    self.headers[vals[0]] = vals[1]
                # We're done with header fields. Onto content
                # Check for query string in post request
                elif len(vals) == 1 and self.method == Request.POST:
                    query_str = line.split('?')
                    self.query_params = query_str[0]


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
        self.request = None

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
            link = f'<a href="{ref_name}">{display}</a>\n</li>\n'
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
        """
        Dispatches appropriate method to handle a request.  Could be
        serving a static file, directory listing, or running a
        CGI script.

        """
        try:
            self.request = Request(self.conn)
        # For some reason we keep getting empty requests
        # from the browser.  In that case we'll just return
        # them to the root of the directory

        except RequestParseError:
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            self.send_header('Location', '/')
            self.end_header()
            self.flush_header()
            return None

        path = self.get_path(self.request.path)

        if os.path.isdir(path):
            self.do_directory(path)

        # Check if it's a file
        elif os.path.isfile(path):
            self.do_file(path)

        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Connection', 'close')
            self.end_header()
            self.flush_header()

            self.wfile.write(b"I can't handle that...")

        self.finish()

    def do_directory(self, path):
        html_contents = self.list_dir(path)
        if html_contents is not None:
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Connection', 'close')
            self.end_header()
            self.flush_header()

            self.wfile.write(html_contents.encode('utf-8'))

    def do_file(self, path):
        """
        Handles the response for all file types.  Determines whether to serve file
        contents or if the path is a CGI script that should be executed.

        :param path: An absolute filesystem path
        :type path: str
        """
        # TODO: Need to check if we're in the cgi-bin dir first
        cgi_exts = ['.py', '.cgi']
        cgi_dir = 'cgi-bin'
        base_path, ext = os.path.splitext(path)
        content_type = mimetypes.types_map.get(ext, 'text/plain')
        abs_dir = os.path.dirname(path)
        parent_dir = os.path.basename(abs_dir)
        # First, see if we need to run a cgi script
        if parent_dir in cgi_dir and ext in cgi_exts:
            self.run_cgi(path)

        # Otherwise, treat like regular file
        else:
            f = None
            try:
                f = open(path, 'rb')

            except OSError:
                # TODO: do error handling
                self.send_response(HTTPStatus.NOT_FOUND)

            if f is not None:
                f_size = os.path.getsize(path)

                self.send_response(HTTPStatus.OK)
                self.send_header('Content-Type', content_type)
                self.send_header('Connection', 'close')
                self.send_header('Content-Length', f_size)
                self.end_header()
                self.flush_header()

                self.wfile.write(f.read())

    def run_cgi(self, path):
        """
        Executes a CGI script in a separate process and writes the output
        into the response buffer.

        :param path: An absolute filesystem path
        :type path: str
        """
        param_str = self.request.query_params
        p = None
        out = b''
        if param_str:
            field, calc_str = param_str.split("=")

            if calc_str:
                calc_str = parse.unquote_plus(calc_str)
                p = subprocess.Popen(['python', path, calc_str],
                                     stdout=subprocess.PIPE)
        else:
            p = subprocess.Popen(['python', path], stdout=subprocess.PIPE)
        if p is not None:
            out, err = p.communicate()

        if out:
            self.send_response(HTTPStatus.OK)
        else:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            out = b'''
                <html>
                <body>
                <h2>I'm not sure what went wrong....</h2>
                </body>
                </html>
            '''
        f2 = io.BytesIO(out)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Connection', 'close')
        self.send_header('Content-Length', len(out))
        self.end_header()
        self.flush_header()
        self.wfile.write(f2.read())

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


class RequestError(Exception):
    def __init__(self, request, msg=None):
        if msg is None:
            msg = f'An error occurred with request:\n{request}'

        super(RequestError, self).__init__(msg)
        self.request = request


class RequestParseError(RequestError):
    def __init__(self, req, msg=None):
        super(RequestParseError, self).__init__(req, msg)


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
