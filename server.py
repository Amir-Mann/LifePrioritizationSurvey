

from http.server import HTTPServer, SimpleHTTPRequestHandler

from io import BytesIO
import os


ALLOWED_PAGES = ["HTMLs/images" + "/" + f for f in os.listdir("HTMLs/images") if os.path.isfile(os.path.join("HTMLs/images", f))]

ALLOWED_PAGES = ALLOWED_PAGES + ["/" + page for page in ALLOWED_PAGES]

PAGES_NAMES = {
    "dry_survay": ["", "HTMLs/dry_survay.html", "dry_survay.html", "dry_survay"],
    "interactive_story": ["HTMLs/interactive_story.html", "interactive_story.html", "interactive_story"],
    "statistics": ["HTMLs/statistics.html", "statistics.html", "statistics"]
}
for key, values in PAGES_NAMES.items():
    for v in values[:]:
        values.append("/" + v)


class EthicalHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        print(f"OURLOG: Handling request for {self.path}")
        
        if self.path in PAGES_NAMES["dry_survay"]:
            self.do_GET_dry_survay()
        elif self.path in PAGES_NAMES["interactive_story"]:
            self.do_GET_interactive_story()
        elif self.path in PAGES_NAMES["statistics"]:
            self.do_GET_statistics()
        elif self.path in ALLOWED_PAGES:
            return super().do_GET()
        else:
            print(f"OURLOG: illeagal request to {self.path}")

    def do_GET_dry_survay(self):
        self.path = 'HTMLs/dry_survay.html'
        print(f"OURLOG: dry_survay: Change path to {self.path}")
        return super().do_GET()

    def do_GET_interactive_story(self):
        self.path = 'HTMLs/interactive_story.html'
        print(f"OURLOG: interactive_story: Change path to {self.path}")
        return super().do_GET()
    
    def do_GET_statistics(self):
        self.path = 'HTMLs/statistics.html'
        print(f"OURLOG: statistics: Change path to {self.path}")
        return super().do_GET()
    
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