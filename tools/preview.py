#!/usr/bin/env python3
"""Serve public/ the way the live site actually serves it.

    python3 tools/preview.py        # then open http://localhost:8080

Python's own `python3 -m http.server` is close, but it gets two things wrong,
and both of them are things you would want to catch before publishing:

  * Cloudflare drops the .html from an address, so the live site answers
    /install. Plain http.server does not, so the "Installing" link in the
    navigation comes back not-found in a preview — the one link most worth
    checking.
  * Cloudflare shows our own 404.html for an address that does not exist.
    Plain http.server shows its own gray error page instead.

Stop it with Ctrl+C.
"""

import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "public"
PORT = 8080


class LikeCloudflare(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = Path(super().translate_path(path))
        # /install -> install.html, the way the live site answers it.
        if not local.exists() and not local.suffix:
            with_html = local.with_suffix(".html")
            if with_html.is_file():
                return str(with_html)
        return str(local)

    def send_error(self, code, message=None, explain=None):
        page = ROOT / "404.html"
        if code == 404 and page.is_file():
            body = page.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def end_headers(self):
        # Never let a browser hold on to an old copy while you are working.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def main():
    handler = partial(LikeCloudflare, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Serving {ROOT} at http://localhost:{PORT}")
        print("Addresses work the same as the live site. Ctrl+C to stop.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
