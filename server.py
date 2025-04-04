import http.server
import socketserver
import sys
import os
from pathlib import Path

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
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
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

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