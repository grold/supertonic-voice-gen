import http.server
import socketserver
import socket
import time

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()

PORT = 8080
IP = get_local_ip()

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    def do_GET(self):
        print(f"DEBUG: Received GET request for {self.path}")
        return super().do_GET()

print(f"DEBUG: Starting test server at http://{IP}:{PORT}/voice_test.mp3")
print(f"DEBUG: I will stay alive for 120 seconds. Please try to open this URL on your phone or computer.")

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
    start_time = time.time()
    while time.time() - start_time < 120:
        httpd.handle_request()
