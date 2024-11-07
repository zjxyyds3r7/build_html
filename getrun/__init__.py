import contextlib
import os
import socket
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler
from http.server import ThreadingHTTPServer


class runHttp(threading.Thread):
    def __init__(self, port, dic):
        threading.Thread.__init__(self)
        self.port = port
        self.dic = dic

    def run(self):
        run(port=self.port, directory=self.dic, bind='0.0.0.0')


class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        print(self.server_address)
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<html><head><title>Home Page</title></head><body><h1>Welcome to the server!</h1><p>Please access other directories.</p></body></html>")
        else:
            super().do_GET()


def run(server_class=DualStackServer,
        port=8000,
        bind='127.0.0.1',
        directory=os.getcwd()):
    """Run an HTTP server on port 8000 (or the port argument).

    Args:
        server_class (_type_, optional): Class of server. Defaults to DualStackServer.
        port (int, optional): Specify alternate port. Defaults to 8000.
        bind (str, optional): Specify alternate bind address. Defaults to '127.0.0.1'.
        cgi (bool, optional): Run as CGI Server. Defaults to False.
        directory (_type_, optional): Specify alternative directory. Defaults to os.getcwd().
    """

    handler_class = partial(CustomHandler, directory=directory)
    with server_class((bind, port), handler_class) as httpd:
        print(
            f"Serving HTTP on {bind} port {port} "
            f"(http://{bind}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
