from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO
import os
from functools import partial

# List of allowed pages for direct access from the HTMLs/images directory
ALLOWED_PAGES_FOR_DIRECT_ACCESS = ["HTMLs/images" + "/" + f for f in os.listdir("HTMLs/images") if os.path.isfile(os.path.join("HTMLs/images", f))]

# Mapping of pages names to possible variation of paths that might mean them
PAGES_NAMES = {
    "dry_survey": ["", "HTMLs/dry_survey.html", "dry_survey.html", "dry_survey"],
    "interactive_story": ["HTMLs/interactive_story.html", "interactive_story.html", "interactive_story"],
    "statistics": ["HTMLs/statistics.html", "statistics.html", "statistics"]
}

# Add paths with leading slashes
ALLOWED_PAGES_FOR_DIRECT_ACCESS = ALLOWED_PAGES_FOR_DIRECT_ACCESS + ["/" + page for page in ALLOWED_PAGES_FOR_DIRECT_ACCESS]
for key, values in PAGES_NAMES.items():
    for v in values[:]:
        values.append("/" + v)

# Dictionary mapping paths for simple redirection
SIMPLE_REDIRACTION_PATHS = {
    image.replace("HTMLs/", "") : image for image in ALLOWED_PAGES_FOR_DIRECT_ACCESS
}
SIMPLE_REDIRACTION_PATHS["/favicon.ico"] = "HTMLs/images/LifePrioratizationSymbol.png"
SIMPLE_REDIRACTION_PATHS["favicon.ico"] = "HTMLs/images/LifePrioratizationSymbol.png"


# Constants for dataset
CSV_FILE_PATH = "entries.csv"
FIELD_NAMES = [
    "Name", "Occupation", "Age", "Gender", "Ethnicity", "Criminal Record", "Medical Record", "Family Situation"
]
PERSONALS_TO_SAVE = [
    "A", "B", "C", "D", "E", "F", "G"
]
DATABASE_FIELDS = ["IP", "ID"] + [field + " (Survey)" for field in FIELD_NAMES] + [field + " (Story)" for field in FIELD_NAMES] + PERSONALS_TO_SAVE


class Database(object):
    """Represents a simple database to store and manipulate data."""

    def __init__(self):
        # Initialize and load data from CSV file
        with open(CSV_FILE_PATH, "r") as f:
            self.database = [line.split(",") for line in f.read().split("\n")]
        self.database_headers = self.database[0]
        assert all(map(lambda tup: tup[0] == tup[1], zip(self.database_headers, DATABASE_FIELDS))), f"<ismatch headers to fields: {list(zip(self.database_headers, DATABASE_FIELDS))}"
        self.database = [[line[0]] + [int(value) for value in line[1:]] for line in self.database[1:]]
        self.entries_count = len(self.database)
        self.id_index = self.database_headers.index("ID")
        
        # Calculate runtime statistics
        self.averages = [0 for _ in self.database_headers[self.id_index + 1:]]
        self.next_available_id = 1
        for line in self.database:
            assert len(line) == len(DATABASE_FIELDS), f"Invalid line length in dataves: {len(line)=} {len(DATABASE_FIELDS)=}"
            for i, value in enumerate(line[self.id_index + 1:]):
                self.averages[i] += value
            if line[self.id_index] >= self.next_available_id:
                self.next_available_id = line[self.id_index] + 1
        self.averages = [sum_value / self.entries_count for sum_value in self.averages]

        # Dictionary for temporary entries not yet inserted
        self.not_inserted = {}
        
        print("OURLOG: Loaded database.")
    
    def register_dry_survey_submition(self, params):
        for field in FIELD_NAMES:
            if field not in params:
                print(f"OURLOG: Dry survey submition is missing field '{field}'")
                return None
            if params[field] not in ("0", "1"):
                print(f"OURLOG: Dry survey submition field '{field}' is not 0 or 1 but {params[field]}")
                return None
        expected_fields_count = len(FIELD_NAMES)
        if len(params.keys()) != expected_fields_count:
            print(f"OURLOG: Dry survey submition with {len(params.keys())} values instead of {expected_fields_count}")
            return None
        
        new_id = self.next_available_id
        self.next_available_id += 1
        
        self.not_inserted[new_id] = {field + " (Survey)" : val for field, val in params.items()}
        self.not_inserted[new_id]["ID"] = str(new_id)
        print(new_id)
        
        return new_id
    
    def register_interactive_story_submition(self, params, ip_address):
        if "ID" not in params:
            print(f"OURLOG: Interactive story submition is missing field 'ID'")
            return None
        
        for field in FIELD_NAMES + PERSONALS_TO_SAVE:
            if field not in params:
                print(f"OURLOG: Interactive story submition is missing field '{field}'")
                return None
            if params[field] not in ("0", "1"):
                print(f"OURLOG: Interactive story submition field '{field}' is not 0 or 1 but {params[field]}")
                return None
        expected_fields_count = len(FIELD_NAMES) + len(PERSONALS_TO_SAVE) + 1
        if len(params.keys()) != expected_fields_count:
            print(f"OURLOG: Interactive story submition with {len(params.keys())} values instead of {expected_fields_count}")
            return None
        
        new_id = int(params["ID"])
        if new_id not in self.not_inserted:
            print(f"OURLOG: Interactive story submition has ID which is not registered as having filled the survey or that has finished the website entirly.")
            return None
        
        choices = self.not_inserted[new_id]
        del self.not_inserted[new_id]
        
        choices["IP"] = ip_address
        for field in FIELD_NAMES:
            choices[field + " (Story)"] = params[field]
        for name in PERSONALS_TO_SAVE:
            choices[name] = params[name]
        
        new_line = [choices[field] for field in self.database_headers]
        with open(CSV_FILE_PATH, "a") as csv:
            csv.write("\n" + ",".join(new_line))
        
        self.averages = [(avg * self.entries_count + int(val)) / self.entries_count 
                         for avg, val in zip(self.averages, new_line[self.id_index + 1:])]
        
        self.database.append(new_line)
                
        return choices


class EthicalHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler with database integration. 
       A signle instance is created for each request with shared db field."""

    def __init__(self, db, *args, **kwargs):
        self.db = db
        self.original_path = None
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        self.original_path = self.path
        print(f"OURLOG: Handling request for '{self.path}'")
        
        # Parse GET parameters
        if "?" in self.path:
            i = self.path.index("?") + 1
            params = dict([tuple(p.split("=")) for p in self.path[i:].replace("%20", " ").replace("_", " ").split("&")])
            self.path = self.path[:i - 1]
        else:
            params = []

        # Route to appropriate page / function handler based on path
        if self.path in PAGES_NAMES["dry_survey"]:
            return self.do_GET_dry_survey(params)
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
            self.do_GET_invalid_page()

    # Handle GET request for dry survey page
    def do_GET_dry_survey(self, params):
        self.path = 'HTMLs/dry_survey.html'
        return super().do_GET()

    # Handle GET request for interactive story page
    def do_GET_interactive_story(self, params):
        
        new_id = self.db.register_dry_survey_submition(params)
        if not new_id:
            return self.do_GET_invalid_page("Denied ileagal 'dry survey' submition.")
        
        # Here should be the code for getting the interactive story.
        # It should use the new_id somehow and send back with the parameter ID={new_id} in when clicking the submit button
        # Right now its just returns the interactive story example HTML
        self.path = 'HTMLs/interactive_story.html'
        return super().do_GET()

    # Handle GET request for statistics page
    def do_GET_statistics(self, params):
        choises = self.db.register_interactive_story_submition(params, self.client_address[0])
        if not choises:
            return self.do_GET_invalid_page("Denied ileagal 'interactive story' submition.")
        
        # Here should be the code for dynamicly creating the statistics html based on self.db.averages and choises
        # Right now its just returns the statistics example HTML
        self.path = 'HTMLs/statistics.html'
        return super().do_GET()

    def do_GET_invalid_page(self, text=None):
        if not text:
            extra_info =  f" (was reformated as '{self.path}')" if self.path != self.original_path else ""
            print(f"OURLOG: illegal request to '{self.original_path}'{extra_info} was blocked. If you think this a mistake talk to Amir")
        else:
            print(f"OURLOG: {text}")
        
    
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
    print("OURLOG: serving...\n")
    httpd.serve_forever()