import http.server
import urllib.request
import sys

class LoadBalancerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Forward the request to the backend server on port 8000
        url = f'http://localhost:8000{self.path}'
        try:
            with urllib.request.urlopen(url) as response:
                # Read response from the backend server
                body = response.read()
                status = response.status
                headers = response.headers

                # Send the response back to the client
                self.send_response(status)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(body)

                # Log the request and response
                client_ip = self.client_address[0]
                request_line = self.requestline
                request_headers = self.headers

                print(f"Received request from {client_ip}")
                print(request_line)
                print(request_headers)
                print(f"Response from server: HTTP/{response.version} {response.status} {response.reason}")
                print(body.decode())
        except Exception as e:
            self.send_error(500, f'Error contacting backend server: {e}')

if __name__ == "__main__":
    port = 80  # Default port for load balancer
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 80.")

    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, LoadBalancerHandler)
    print(f"Load Balancer running on port {port}")
    httpd.serve_forever()
