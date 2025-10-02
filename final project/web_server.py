"""
Simple web server to serve the HTML interface
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def start_web_server(port=3000):
    """Start a simple HTTP server to serve the web interface"""
    
    # Change to the directory containing the HTML file
    os.chdir(Path(__file__).parent)
    
    # Create a custom handler that serves the HTML file
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '/index.html':
                self.path = '/web_interface.html'
            return super().do_GET()
    
    try:
        with socketserver.TCPServer(("", port), CustomHandler) as httpd:
            print("🌐 Web Interface Server Starting...")
            print("=" * 50)
            print(f"📱 Web Interface: http://localhost:{port}")
            print("🔗 API Documentation: http://localhost:8000/docs")
            print("=" * 50)
            print("Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Try to open the browser automatically
            try:
                webbrowser.open(f'http://localhost:{port}')
                print("🚀 Browser opened automatically")
            except:
                print("💡 Please open your browser and go to the URL above")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Web server stopped")
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"❌ Port {port} is already in use. Trying port {port + 1}")
            start_web_server(port + 1)
        else:
            print(f"❌ Error starting web server: {e}")

if __name__ == "__main__":
    start_web_server()
