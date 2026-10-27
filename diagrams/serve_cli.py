"""Serve only Mermaid CLI's HTML shell over policy-allowed loopback HTTP."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import sys

html = Path(sys.argv[1]).read_bytes()
port_file = Path(sys.argv[2])


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if self.path != "/index.html":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, *_):
        pass


server = HTTPServer(("127.0.0.1", 0), Handler)
port_file.write_text(str(server.server_port))
server.serve_forever()
