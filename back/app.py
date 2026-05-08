from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HOST = "0.0.0.0"
PORT = 8080
RESPONSE_BODY = b"Hello from Effective Mobile!"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request(send_body=True)

    def do_HEAD(self):
        self.handle_request(send_body=False)

    def handle_request(self, send_body):
        path = urlparse(self.path).path

        if path == "/":
            self.send_text_response(200, RESPONSE_BODY, send_body)
        else:
            self.send_text_response(404, b"Not Found", send_body)

    def send_text_response(self, status_code, body, send_body):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        if send_body:
            self.wfile.write(body)
    def log_message(self, fmt, *args):
        print(f"{self.client_address[0]} - {fmt % args}", flush=True)

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), RequestHandler)
    print(f"Backend server is running on {HOST}:{PORT}", flush=True)
    server.serve_forever()
