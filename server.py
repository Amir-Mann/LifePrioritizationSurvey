

from http.server import HTTPServer, SimpleHTTPRequestHandler

from io import BytesIO
import os


ALLOWED_PAGES = [
    "HTMLs/dry_survay.html",
    "HTMLs/interactive_story.html",
    "HTMLs/statistics.html"
] + [os.path.join("HTMLs/images", f) for f in os.listdir("HTMLs/images") if os.path.isfile(os.path.join("HTMLs/images", f))]

ALLOWED_PAGES = ALLOWED_PAGES + ["/" + page for page in ALLOWED_PAGES]
class EthicalHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        print(f"OURLOG: Handling request for {self.path}")
        
        if self.path == '/':
            self.path = 'HTMLs/dry_survay.html'
            print(f"OURLOG: Change path to {self.path}")
        
        if self.path in ALLOWED_PAGES:
            return super().do_GET()
        else:
            print(f"OURLOG: illeagal request to {self.path}")

    def do_POST(self):
        # Irelevent example code
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8000), EthicalHTTPRequestHandler)
    print("serving...")
    httpd.serve_forever()