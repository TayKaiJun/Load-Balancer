import http.server
import socketserver
import sys

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Log the request details
        client_ip = self.client_address[0]
        request_line = self.requestline
        headers = str(self.headers)

        print(f"Received request from {client_ip}")
        print(request_line)
        print(headers.strip())
        
        # Send a response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, world!\n")

        # Log the response message
        print("Replied with a hello message")

if __name__ == "__main__":
    # Get the port number from the command-line arguments
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")

    Handler = CustomHandler

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()
