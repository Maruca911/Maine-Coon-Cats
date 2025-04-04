import http.server
import socketserver
import os
import mimetypes
from datetime import datetime, timedelta
import socket

def find_available_port(start_port=8000, max_port=8100):
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports between {start_port} and {max_port}")

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/index.html'
        
        # Handle blog path
        elif self.path == '/blog':
            self.path = '/blog/index.html'
        
        # Check if file exists
        file_path = self.translate_path(self.path)
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return
        
        # Set cache headers
        self.set_cache_headers(file_path)
        
        # Set content type
        content_type = self.guess_type(file_path)
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        
        # Serve the file
        try:
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        except Exception as e:
            print(f"Error serving file {file_path}: {e}")
            self.send_error(500, "Internal server error")

    def set_cache_headers(self, file_path):
        # Set long cache for static files
        if any(file_path.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico']):
            self.send_header('Cache-Control', 'public, max-age=31536000')
            self.send_header('Expires', (datetime.now() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        else:
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')

    def guess_type(self, path):
        content_type, _ = mimetypes.guess_type(path)
        return content_type or 'text/html'

def run():
    port = find_available_port()
    handler_class = MyHttpRequestHandler
    server_class = http.server.HTTPServer
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    run() 