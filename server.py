#!/usr/bin/env python3
"""Tiny local server for Volleyball_Entry_Desk.html.
Serves this folder (so the page can read employee.csv) and lets the page
save player.csv in the same folder. Run:  python3 server.py  [port]
Then open http://localhost:8000/Volleyball_Entry_Desk.html
"""
import http.server, os, sys, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_PUT(self):
        if self.path.split("?")[0] != "/player.csv":
            self.send_error(403, "Only player.csv can be written")
            return
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        tmp = os.path.join(ROOT, "player.csv.tmp")
        try:
            with open(tmp, "wb") as f:
                f.write(data)
            os.replace(tmp, os.path.join(ROOT, "player.csv"))
        except OSError as e:  # e.g. file open in Excel on Windows
            self.send_error(500, str(e))
            return
        self.send_response(204)
        self.end_headers()

if __name__ == "__main__":
    url = f"http://localhost:{PORT}/Volleyball_Entry_Desk.html"
    print("Serving", ROOT, "\nOpen", url, "\nPress Ctrl+C to stop.")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
