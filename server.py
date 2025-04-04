import http.server
import socketserver
import os
import sys
import socket
import json
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", 8000))
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_POST(self):
        if self.path == '/generate-meal-plan':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = parse_qs(post_data.decode('utf-8'))
            
            try:
                # Basic response for now, we'll implement the meal planner later
                result = {
                    'success': True,
                    'message': 'Meal plan generation will be implemented soon'
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'message': str(e)
                }).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/index.html'
        
        # Handle blog paths
        if self.path.startswith('/blog/'):
            # Remove trailing slash if present
            path = self.path.rstrip('/')
            
            # Try different file extensions
            possible_paths = [
                path,
                path + '.html',
                path + '/index.html'
            ]
            
            for try_path in possible_paths:
                file_path = try_path[1:]  # Remove leading slash
                if os.path.isfile(file_path):
                    self.path = try_path
                    break
        
        try:
            file_to_open = open(self.path[1:], 'rb').read()
            self.send_response(200)
        except:
            file_to_open = b'File not found'
            self.send_response(404)
        
        self.end_headers()
        self.wfile.write(file_to_open)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def find_available_port(start_port):
    port = start_port
    while is_port_in_use(port):
        port += 1
    return port

def run():
    try:
        # Try to use the default port
        if is_port_in_use(PORT):
            print(f"Port {PORT} is in use. Finding an available port...")
            port = find_available_port(PORT)
            print(f"Using port {port} instead.")
        else:
            port = PORT

        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving at http://localhost:{port}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run() 