import http.server
import http.client
import socketserver
import os
import sys

PORT = 3000
BACKEND_PORT = 8000
STATIC_DIR = r'c:\Users\vishn\AndroidStudioProjects\DynAcuityWeb'

class UnifiedHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.proxy_request('GET')
        else:
            self.serve_static()

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_request('POST')
        else:
            self.send_error(404)

    def do_PATCH(self):
        if self.path.startswith('/api/'):
            self.proxy_request('PATCH')
        else:
            self.send_error(404)

    def do_PUT(self):
        if self.path.startswith('/api/'):
            self.proxy_request('PUT')
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        if self.path.startswith('/api/'):
            self.proxy_request('OPTIONS')
        else:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

    def serve_static(self):
        # Strip query parameters for local file lookup
        full_path = self.path.split('?')[0]
        if full_path == "" or full_path == "/":
            full_path = "/index.html"
            
        file_path = os.path.abspath(os.path.join(STATIC_DIR, full_path.lstrip('/')))
        
        # Security check: ensure file is within STATIC_DIR
        if not file_path.startswith(os.path.abspath(STATIC_DIR)):
            self.send_error(403, "Access denied")
            return

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, 'index.html')

        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(f"DEBUG Serving Static: {file_path}", flush=True)
            self.send_response(200)
            if file_path.endswith('.html'):
                self.send_header('Content-Type', 'text/html')
            elif file_path.endswith('.js'):
                self.send_header('Content-Type', 'application/javascript')
            elif file_path.endswith('.css'):
                self.send_header('Content-Type', 'text/css')
            
            self.send_header('Content-Length', str(os.path.getsize(file_path)))
            self.end_headers()
            try:
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                print(f"DEBUG Error writing response: {str(e)}", flush=True)
        else:
            print(f"DEBUG File Not Found: {file_path}", flush=True)
            self.send_error(404, "File not found")

    def proxy_request(self, method):
        print(f"DEBUG Proxying: {method} {self.path}", flush=True)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None
        
        headers = {key: value for key, value in self.headers.items() if key.lower() != 'host'}
        headers['Host'] = f'127.0.0.1:{BACKEND_PORT}'

        try:
            conn = http.client.HTTPConnection('127.0.0.1', BACKEND_PORT, timeout=10)
            conn.request(method, self.path, body, headers)
            res = conn.getresponse()

            print(f"DEBUG Backend Response: {res.status}", flush=True)
            self.send_response(res.status)
            for key, value in res.getheaders():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(res.read())
        except Exception as e:
            print(f"DEBUG Proxy Error: {str(e)}", flush=True)
            self.send_error(502, f"Proxy error: {str(e)}")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    os.chdir(STATIC_DIR)
    sys.stdout.reconfigure(line_buffering=True)
    try:
        with ThreadedTCPServer(("0.0.0.0", PORT), UnifiedHandler) as httpd:
            print(f"Unified Server (Static + API Proxy) at port {PORT}", flush=True)
            print(f"Serving files from: {STATIC_DIR}", flush=True)
            print(f"Proxying /api/* to: 127.0.0.1:{BACKEND_PORT}", flush=True)
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 10048:
            print(f"ERROR: Port {PORT} is already in use.", file=sys.stderr, flush=True)
            print(f"Please close any other python processes and try again.", file=sys.stderr, flush=True)
            # Find and suggest the PID (manual step for user)
            sys.exit(1)
        else:
            raise e
