import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os

PORT = 8000

class MLflowProxyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quiet down logging a bit
        print(f"[Proxy Server] {format % args}")

    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse target URL and payload from the UI request
                request_data = json.loads(post_data)
                target_url = request_data.get('target_url', 'http://localhost:1234/invocations')
                payload = request_data.get('payload')
                
                print(f"[Proxy Server] Forwarding prediction request to: {target_url}")
                
                # Forward request to the MLflow model serving API
                req = urllib.request.Request(
                    target_url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=5) as response:
                    res_body = response.read()
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(res_body)
                    
            except urllib.error.HTTPError as e:
                # MLflow returned an error (e.g. 400 Bad Request)
                error_body = e.read().decode('utf-8')
                print(f"[Proxy Server] HTTP Error from MLflow: {e.code} - {error_body}")
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(error_body.encode('utf-8'))
                
            except urllib.error.URLError as e:
                # Connection failure (MLflow not running)
                print(f"[Proxy Server] Connection error to MLflow: {e.reason}")
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_msg = {"error": f"Could not connect to MLflow serving endpoint. Make sure it is running on that port! (Reason: {e.reason})"}
                self.wfile.write(json.dumps(error_msg).encode('utf-8'))
                
            except Exception as e:
                print(f"[Proxy Server] Unexpected error: {str(e)}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_msg = {"error": f"Internal proxy error: {str(e)}"}
                self.wfile.write(json.dumps(error_msg).encode('utf-8'))
        else:
            # Fallback for other POST requests
            super().do_POST()

    def do_OPTIONS(self):
        # Support CORS preflight if needed
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    # Serve from the directory where server.py lives
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Allow port reuse to avoid 'Address already in use' errors
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), MLflowProxyHandler) as httpd:
        print("\n" + "="*50)
        print(f"  MLflow UI Client Server started at: http://localhost:{PORT}")
        print("  Press CTRL+C to stop.")
        print("="*50 + "\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down proxy server...")
