import http.server
import socketserver
import os
import sys

# Configure UTF-8 encoding for standard output if supported
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Prevent aggressive browser caching during development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean request logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]} {args[1]} -> Status {args[2]}\n")

def run_server():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}"
            print("=" * 60)
            print(">>> SPACE DEFENDER - LOCAL GAME SERVER")
            print(f">>> Serving at: {url}")
            print(">>> Open your browser to play directly: http://localhost:8000")
            print(">>> Press Ctrl+C in this terminal to stop the server.")
            print("=" * 60)
            sys.stdout.flush()
            
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e) or getattr(e, 'errno', None) in (98, 10048):
            print(f"\n[INFO] Port {PORT} is already in use. Space Defender is already running!")
            print(f">>> Visit: http://localhost:{PORT}")
        else:
            raise e
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by user.")

if __name__ == "__main__":
    run_server()
