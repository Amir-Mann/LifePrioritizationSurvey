from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO
import os
from functools import partial

# List of allowed pages for direct access from the HTMLs/images directory
ALLOWED_PAGES_FOR_DIRECT_ACCESS = ["HTMLs/images" + "/" + f for f in os.listdir("HTMLs/images") if os.path.isfile(os.path.join("HTMLs/images", f))]

# Dictionary mapping paths for simple redirection
SIMPLE_REDIRACTION_PATHS = {
    "/favicon.ico": "HTMLs/images/LifePrioratizationSymbol.png"
}

# Mapping of pages names to possible variation of paths that might mean them
PAGES_NAMES = {
    "dry_survay": ["", "HTMLs/dry_survay.html", "dry_survay.html", "dry_survay"],
    "interactive_story": ["HTMLs/interactive_story.html", "interactive_story.html", "interactive_story"],
    "statistics": ["HTMLs/statistics.html", "statistics.html", "statistics"]
}

# Add paths with leading slashes
ALLOWED_PAGES_FOR_DIRECT_ACCESS = ALLOWED_PAGES_FOR_DIRECT_ACCESS + ["/" + page for page in ALLOWED_PAGES_FOR_DIRECT_ACCESS]
for key, values in PAGES_NAMES.items():
    for v in values[:]:
        values.append("/" + v)

# Constants for dataset
CSV_FILE_PATH = "entries.csv"
ID_COLUMN_IN_DB = 0

class Database(object):
    """Represents a simple database to store and manipulate data."""

    def __init__(self):
        # Initialize and load data from CSV file
        with open(CSV_FILE_PATH, "r") as f:
            self.database = [line.split(",") for line in f.read().split("\n")]
        self.database_headers = self.database[0]
        self.database = [[int(value) for value in line] for line in self.database[1:]]
        self.entries_count = len(self.database)
        
        # Calculate runtime statistics
        self.averages = [0 for _ in self.database_headers]
        self.next_available_id = 0
        for line in self.database:
            for i, value in enumerate(line):
                self.averages[i] += value
            if line[ID_COLUMN_IN_DB] >= self.next_available_id:
                self.next_available_id = line[ID_COLUMN_IN_DB] + 1
        self.averages = [sum_value / self.entries_count for sum_value in self.averages]

        # Dictionary for temporary entries not yet inserted
        self.not_inserted = {}
        
        print("OURLOG: Loaded database.")

class EthicalHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler with database integration. 
       A signle instance is created for each request with shared db field."""

    def __init__(self, db, *args, **kwargs):
        self.db = db
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        print(f"OURLOG: Handling request for {self.path}")

        # Parse GET parameters
        if "?" in self.path:
            i = self.path.index("?") + 1
            params = dict([tuple(p.split("=")) for p in self.path[i:].split("&")])
        else:
            params = []

        # Route to appropriate page / function handler based on path
        if self.path in PAGES_NAMES["dry_survay"]:
            return self.do_GET_dry_survay(params)
        elif self.path in PAGES_NAMES["interactive_story"]:
            return self.do_GET_interactive_story(params)
        elif self.path in PAGES_NAMES["statistics"]:
            return self.do_GET_statistics(params)
        elif self.path in SIMPLE_REDIRACTION_PATHS:
            self.path = SIMPLE_REDIRACTION_PATHS[self.path]
            return super().do_GET()
        elif self.path in ALLOWED_PAGES_FOR_DIRECT_ACCESS:
            return super().do_GET()
        else:
            print(f"OURLOG: illegal request to {self.path}")

    # Handle GET request for dry survey page
    def do_GET_dry_survay(self, params):
        self.path = 'HTMLs/dry_survay.html'
        print(f"OURLOG: dry_survay: Change path to {self.path}")
        return super().do_GET()

    # Handle GET request for interactive story page
    def do_GET_interactive_story(self, params):
        self.path = 'HTMLs/interactive_story.html'
        print(f"OURLOG: interactive_story: Change path to {self.path}")
        return super().do_GET()

    # Handle GET request for statistics page
    def do_GET_statistics(self, params):
        self.path = 'HTMLs/statistics.html'
        print(f"OURLOG: statistics: Change path to {self.path}")
        return super().do_GET()

    def do_POST(self):
        # Irelevent example code copied from internet
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
    db = Database()
    handler_cls = partial(EthicalHTTPRequestHandler, db)
    httpd = HTTPServer(('localhost', 8000), handler_cls)
    print("OURLOG: serving...")
    httpd.serve_forever()