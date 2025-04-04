import http.server
import socketserver
import sys
import os
from pathlib import Path
import mimetypes
from datetime import datetime, timedelta

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/index.html'
        # Handle blog paths
        elif self.path.startswith('/blog/'):
            # Check if the path ends with a trailing slash
            if not self.path.endswith('/'):
                self.path += '/'
            # Add index.html to the path
            self.path += 'index.html'

        # Check if file exists
        file_path = self.translate_path(self.path)
        if not os.path.exists(file_path):
            self.path = '/404.html'
            self.send_response(404)
        else:
            self.send_response(200)

        # Set cache headers for static files
        if self.path.startswith(('/static/', '/css/', '/js/', '/images/')):
            self.send_header('Cache-Control', 'public, max-age=31536000')
            self.send_header('Expires', (datetime.now() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        else:
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')

        # Set content type
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type:
            self.send_header('Content-Type', content_type)
        else:
            self.send_header('Content-Type', 'text/html')

        self.end_headers()

        # Send the file
        try:
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        except Exception as e:
            print(f"Error serving {file_path}: {e}")
            self.send_error(500, "Internal Server Error")

def run(port=8000):
    # Set the directory to serve files from
    os.chdir(str(Path(__file__).parent))
    
    # Create the server
    handler = MyHttpRequestHandler
    server_address = ('', port)
    httpd = socketserver.TCPServer(server_address, handler)
    
    print(f"Serving at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    # Get port from command line argument or use default
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run(port) 