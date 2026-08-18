#!/usr/bin/env python3
"""HTTP Smuggle — real mini-challenge (http-smuggle)."""
import base64, hashlib, hmac, json, os, re, sqlite3, sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote, quote

sys.path.insert(0, "/challenge/_shared")
from fetch_material import fetch_material

CHALLENGE_KEY = os.environ.get("CHALLENGE_KEY", 'desync-frontier')
_MAT = {}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain", headers=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        data = body if isinstance(body, bytes) else body.encode()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/flag":
            return self._send(200, _MAT.get("delivery_blob", "") + "\n")
        if p.path == "/admin":
            return self._send(200, f"admin ok; key={CHALLENGE_KEY}\n")
        self._send(200, "HTTP smuggle lab: POST /backend  GET /admin  /flag\n")

    def do_POST(self):
        p = urlparse(self.path)
        if p.path == "/flag":
            return self._send(200, _MAT.get("delivery_blob", "") + "\n")
        if p.path != "/backend":
            return self._send(404, "no\n")
        cl = self.headers.get("Content-Length", "")
        te = self.headers.get("Transfer-Encoding", "")
        length = int(cl or 0)
        body = self.rfile.read(length).decode(errors="replace") if length else ""
        smuggled = ""
        if te.lower() == "chunked" and cl:
            if "GGET /admin" in body or "GET /admin" in body.split("\r\n", 1)[-1]:
                smuggled = "GET /admin"
        if smuggled or "GET /admin" in body:
            return self._send(200, f"backend desync; smuggled={smuggled or 'GET /admin'}; key={CHALLENGE_KEY}\n")
        return self._send(200, f"backend ok (CL={cl} TE={te})\n")


def main():
    _MAT.update(fetch_material())
    print('HTTP Smuggle on :8080')
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

if __name__ == "__main__":
    main()
