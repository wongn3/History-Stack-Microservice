from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

history: list[str] = []  # Most recent → least recent
home_page: str | None = None

def add_to_history(url):
    global history
    
    if url in history: #checks if the url is already in the history list
        history.remove(url) #removes it if so
    
    history.insert(0, url) #adds it to front

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self): #will run when a GET request is made to the server
        parsed = urlparse(self.path) #splits url into the path and query parameters 
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/setHome": #checks if user wants to reset the home page
            url = params.get("url", [None])[0] #gets url and returns none if it doesn't exist
            
            if not url:
                return self.respond({"error": "Missing url parameter"}, 400) #returns error if url parameter is missing

            global home_page
            home_page = url #updates home page

            history.clear() #resets history
            
            return self.respond({"message": "Home page set", "home": url}) #Json response

        elif path == "/visit": #checks if user wants to visit a page
            url = params.get("url", [None])[0] #gets url
            
            if not url:
                return self.respond({"error": "Missing url parameter"}, 400) #if url parameter is missing, return error

            if url == home_page:
                return self.respond({"message": "Homepage Ignored", "url": url}) #ignores homepage visits

            add_to_history(url) #add to history
            
            return self.respond({"message": "Recorded", "url": url}) #Json response

        elif path == "/history": #checks if user wants to view history
            return self.respond({"history": history})
        
        elif path == "/remove":
            if not history:
                return self.respond({"error": "History is empty"}, 400) #Json response

            removed = history.pop(0) #removes most recent url from history
            return self.respond({"message": "Removed most recent", "removed": removed}) #Json response


        else:
            return self.respond({"error": "Unknown endpoint"}, 404) #Json response

    def respond(self, data, status=200): #helps with Json responses
        response = json.dumps(data).encode("utf-8")
        self.send_response(status) #status code
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response) #Json body

def run():
    server = HTTPServer(("localhost", 8080), MyHandler)
    print("Server running on http://localhost:8080")
    server.serve_forever()

if __name__ == "__main__":
    run()